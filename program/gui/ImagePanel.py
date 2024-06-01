import numpy as np
from PIL import Image
from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QPoint

class ImagePanel(QGraphicsView):
    """
    ImagePanel
    
    이미지 뷰, 확대 & 축소
    """
    
    __DEFAULT_IMAGE: np.ndarray = np.array(Image.open('./program/resource/test.png').convert('RGB'), dtype=np.uint8)

    def __init__(self, base:QWidget):
        """
        base -- 부모 위젯
        """
        super().__init__(base)
        self.__image: np.ndarray = ImagePanel.__DEFAULT_IMAGE
        self.__scale: float = 1
        self.setStyleSheet("background-color: black;")
        
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.__scene:QGraphicsScene = QGraphicsScene(self)
        self.__image_item:QGraphicsPixmapItem = QGraphicsPixmapItem()
        self.__scene.addItem(self.__image_item)
        self.setScene(self.__scene)
        
        self.draw_image()
        
    def set_image(self, image: np.ndarray):
        """ 
        이미지는 RGB 순서로 간주함
        
        image -- np.ndarray 이미지
        """
        
        if not isinstance(image, np.ndarray):
            self.__image = ImagePanel.__DEFAULT_IMAGE
        else:
            self.__image = image.astype(np.uint8)
        self.draw_image()
        
    def draw_image(self):
        """
        이미지 그리기
        """
        
        self.__image_item.setPos(0,0)
        self.fitInView(self.__image_item, Qt.AspectRatioMode.KeepAspectRatio)
        self.__scale = 0
        self.__image_item.setPixmap(QPixmap.fromImage(QImage(
            self.__image.data,
            self.__image.shape[1],
            self.__image.shape[0],
            self.__image.shape[1] * 3,
            QImage.Format.Format_RGB888
        )))
        
    def resize_image(self, scale_factor: int, pos: QPoint):
        """
        이미지 리사이즈
        
        scale_factor -- int 이미지 확대 축소 결정.
            scale_factor > 0 확대
            scale_facter < 0 축소
            scale_facter = 0 유지
        pos -- 마우스 포인터 위치
        """
        
        if scale_factor > 0:
            scale_factor = 1.1
        elif scale_factor < 0:
            scale_factor = 0.9
        else:
            return
        
        scale = self.__scale * scale_factor
        if scale < 1.05:
            self.__image_item.setPos(0,0)
            self.fitInView(self.__image_item, Qt.AspectRatioMode.KeepAspectRatio)
            self.__scale = 1
            return
        elif scale > 3:
            scale_factor = 1
        else:
            self.__scale = scale

        old_pos = self.mapToScene(pos)
        self.scale(scale_factor, scale_factor)
        new_pos = self.mapToScene(pos)
        if self.__scale > 1:
            self.__image_item.setPos(self.__image_item.pos() + new_pos - old_pos)
    
    def resize_event(self):
        self.__image_item.setPos(0,0)
        self.fitInView(self.__image_item, Qt.AspectRatioMode.KeepAspectRatio)
        self.__scale = 1
        
    def image_move(self, delta:QPoint):
        """
        이미지 이동
        
        delta -- QPoint 해당 값 만큼 이동
        """
        new_pos = self.__image_item.pos() + delta
        size = self.size()
        width = size.width()//2 * 3
        height = size.height()//2 * 3
        if new_pos.x() > width:
            new_pos.setX(width)
        elif new_pos.x() < -width:
            new_pos.setX(-width)
        if new_pos.y() > height:
            new_pos.setY(height)
        elif new_pos.y() < -height:
            new_pos.setY(-height)
        self.__image_item.setPos(new_pos)
