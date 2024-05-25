import sys
from typing import Type
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtCore import QTimer

from gui.imageLayer import ImageLayer
from gui.ImagePanel import ImagePanel

from core import DataController

class Frame(QWidget):
    """
    프로그램 기반 위젯 생성
    """
    
    __TITLE:str = "Image Classifier"

    def __init__(self, x: int, y: int, width: int, height: int):
        """
        x -- int >= 0
        y -- int >= 0
        width -- int >= 0 
        height -- int >= 0
        """
        super().__init__()
        self.__x:int = x
        self.__y :int= y
        self.__width:int = width
        self.__height:int = height
        self.__image_panel: ImagePanel = ImagePanel(self)
        self.__image_layer: ImageLayer = None # 생각해보자
        
        self.init_ui()
        
    def set_image_layer(self, data_controller:DataController, ImageLayer_:Type[ImageLayer] = ImageLayer):
        """
        Image Layer 생성
        
        data_controller -- DataController
        ImageLayer_ -- ImageLayer (class. not instance)
        """
        self.__image_layer = ImageLayer_(self, self.__image_panel, data_controller)
        self.__image_layer.raise_()
        
    def init_ui(self):
        self.setWindowTitle(self.__TITLE)
        self.setGeometry(self.__x, self.__y, self.__width, self.__height)
        self.setStyleSheet("background-color: black;")

        self.__image_panel.setGeometry(0,0,self.__width, self.__height)
        
    def resizeEvent(self, event:QResizeEvent):
        size = event.size()
        self.__image_layer.setGeometry(0, 0, size.width(), size.height())
        self.__image_panel.setGeometry(0, 0, size.width(), size.height())
        self.__image_panel.resize_event()
        super().resizeEvent(event)
        

# test code
def main():
    app = QApplication(sys.argv)
    main = Frame(100, 100, 500, 500)
    main.show()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    pass