import numpy as np
from PIL import Image
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QSize

class ImagePanel(QLabel):
    """
    ImagePanel
    
    이미지 뷰, 확대 & 축소
    """
    
    __DEFAULT_IMAGE: np.ndarray = np.array(Image.open('./program/resource/test.png').convert('RGB'), dtype=np.uint8)

    def __init__(self, base:QWidget):
        super().__init__(base)
        self.__image: np.ndarray = ImagePanel.__DEFAULT_IMAGE
        self.__scale: float = 1
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: orange;")
        
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
        
    def draw_image(self, n:int = 0, size:QSize = None):
        """
        이미지 그리기
        
        n -- 이미지 확대 축소 비율.
            n > 0 -> 이미지 확대
            n < 0 -> 이미지 축소
            n = 0 -> 그대로
        size -- QSize 조정하고 싶은 크기
        """
        
        self.__scale = self.__scale + n/100 
        if 0.98 < self.__scale < 1.02: self.__scale = 1
        if size is None: 
            size = self.size()
        
        image = self.__resize_image(size)
        self.setPixmap(QPixmap(QImage(
            image.data,
            image.shape[1],
            image.shape[0],
            image.shape[1] * 3,
            QImage.Format.Format_RGB888
        )))

    def __resize_image(self, size:QSize):
        """
        이미지 크기 조정
        
        size -- QSize 조정하고 싶은 크기
        """
            
        height, width, _ = self.__image.shape
        frame_width, frame_height = size.width(), size.height()
        
        if height/frame_height > width/frame_width:
            width = width/height * frame_height
            height = frame_height
        else:
            height = height/width * frame_width
            width = frame_width
            
        width = int(width * self.__scale)
        height = int(height * self.__scale)
        
        if self.__scale > 1:
            x = 0
            y = 0
            if width > frame_width:
                x = (frame_width - width) // 2
            if height > frame_height:
                y = (frame_height - height) // 2
            self.setGeometry(x, y, width, height)
        else:
            self.setGeometry(0, 0, frame_width, frame_height)
            
        return np.array(Image.fromarray(self.__image).resize((width, height), Image.LANCZOS))
        