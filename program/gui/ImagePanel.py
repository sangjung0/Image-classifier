import numpy as np
from PIL import Image
from PyQt5.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem
from PyQt5.QtGui import QPixmap, QImage, QPen, QColor
from PyQt5.QtCore import Qt, QPoint, QRectF

from core.dto import Character

class ImagePanel(QGraphicsView):
    """
    ImagePanel
    
    이미지 뷰, 확대 & 축소
    """
    
    __DEFAULT_IMAGE: np.ndarray = np.array(Image.open('./program/resource/test.png').convert('RGB'), dtype=np.uint8)

    def __init__(self, base:QWidget) -> None:
        """
        base -- 부모 위젯
        """
        super().__init__(base)
        self.__image: np.ndarray = ImagePanel.__DEFAULT_IMAGE
        self.__faces: dict[int:Character] = {}
        self.__face_rect: list[QGraphicsRectItem] = []
        self.__cursor_is_in:bool = True
        self.__scale: float = 1
        self.__image_scale: float = 1
        self.setStyleSheet("background-color: black;")
        
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.__scene:QGraphicsScene = QGraphicsScene(self)
        self.__image_item:QGraphicsPixmapItem = QGraphicsPixmapItem()
        self.__scene.addItem(self.__image_item)
        self.setScene(self.__scene)
        
        self.draw_image()
        
    def set_image(self, face:dict[int:Character], image: np.ndarray) -> None:
        """ 
        이미지는 RGB 순서로 간주함
        
        image -- np.ndarray 이미지
        """
        
        self.remove_faces()
        if not isinstance(image, np.ndarray):
            self.__image = ImagePanel.__DEFAULT_IMAGE
            self.__faces = {}
        else:
            self.__image = image
            self.__faces = face
        self.draw_image()
        self.set_face()
        self.resize_event()
        
    def set_face(self) -> None:
        pen = QPen(QColor(255, 0, 0), 2, Qt.PenStyle.SolidLine)
        for i in range(len(self.__faces)):
            rect = None
            if i >= len(self.__face_rect):
                rect = QGraphicsRectItem()
                rect.setPen(pen)
                self.__face_rect.append(rect)
            else:
                rect = self.__face_rect[i]
            self.__scene.addItem(rect)
        
    def draw_faces(self, x:float, y:float) -> None:
        for i, face in enumerate(self.__faces.values()):
            if i >= len(self.__face_rect): self.set_face()
            rect = self.__face_rect[i]
            fx, fy, width, height = face.get_location()
            rect.setRect(0, 0, width*self.__image_scale, height*self.__image_scale )
            rect.setPos(fx*self.__image_scale+x, fy*self.__image_scale+y)
    
    def remove_faces(self) -> None:
        items = list(set(self.__face_rect) & set(self.__scene.items()))
        for d in items:
            self.__scene.removeItem(d)
        
    def draw_image(self) -> None:
        """
        이미지 그리기
        """
        self.__image_item.setPos(0, 0)
        self.__image_item.setPixmap(QPixmap.fromImage(QImage(
            self.__image.data,
            self.__image.shape[1],
            self.__image.shape[0],
            self.__image.shape[1] * 3,
            QImage.Format.Format_RGB888
        )))
        
    def resize_image(self, scale_factor: int, pos: QPoint) -> None:
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
        if scale < 1:
            scale_factor = 1
        elif scale > 5:
            scale_factor = 1
        else:
            self.__scale = scale

        old_pos = self.mapToScene(pos)
        self.scale(scale_factor, scale_factor)
        new_pos = self.mapToScene(pos)
        pos = self.__image_item.pos() + new_pos - old_pos
        self.__image_item.setPos(pos)
        
        self.draw_faces(pos.x(), pos.y())
            
    def resize_event(self) -> None:

        self.resetTransform()
        self.__scale = 1    
        v_width = self.width()
        v_height = self.height()
        height, width, _ = self.__image.shape
        x, y = 0, 0
        scale = 1
        
        if height/v_height > width/v_width:
            if height >= v_height:
                scale = v_height / height
                x = (v_width - width*scale)//2
            else:
                y = (v_height - height)//2
                x = (v_width - width)//2
        else:
            if width >= v_width:
                scale = v_width / width
                y = (v_height - height*scale)//2
            else:
                y = (v_height - height)//2
                x = (v_width - width)//2
        
        self.__image_scale = scale
        self.__image_item.setScale(scale)
        self.__image_item.setPos(x, y)
        self.__scene.setSceneRect(QRectF(0, 0, v_width, v_height))

        self.draw_faces(x, y)
        
    def image_move(self, delta:QPoint) -> None:
        """
        이미지 이동
        
        delta -- QPoint 해당 값 만큼 이동
        """
        new_pos = self.__image_item.pos() + delta/self.__scale
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

        self.draw_faces(new_pos.x(), new_pos.y())

    def click_event(self, pos:QPoint) -> int:
        scene_pos = self.mapToScene(pos)
        
        for i, rect in enumerate(self.__face_rect):
            if rect.contains(pos - rect.pos()):
                return i