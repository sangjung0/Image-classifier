import sys
from typing import Type
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QResizeEvent, QCloseEvent

from gui.imageLayer import ImageLayer
from gui.ImagePanel import ImagePanel

from core import DataController

class Frame(QWidget):
    """
    프로그램 기반 위젯 생성
    """
    
    __TITLE:str = "Image Classifier"

    def __init__(self, x: int, y: int, width: int, height: int, 
                 ImageLayer_:Type[ImageLayer] = ImageLayer, 
                 data_controller:DataController = None
                ) -> None:
        """
        x -- int >= 0 \n
        y -- int >= 0 \n
        width -- int >= 0 \n
        height -- int >= 0 \n
        ImageLayer_ -- ImageLayer (class. not instance) \n
        data_controller -- DataController \n
        """
        super().__init__()
        self.__x:int = x
        self.__y :int= y
        self.__width:int = width
        self.__height:int = height
        self.__image_panel: ImagePanel = ImagePanel(self)
        self.__image_layer: ImageLayer = ImageLayer_(self, self.__image_panel, DataController([],[]) if data_controller is None else data_controller)
        
        self.init_ui()
        
    def init_ui(self) -> None:
        self.setWindowTitle(self.__TITLE)
        self.setGeometry(self.__x, self.__y, self.__width, self.__height)
        #self.setStyleSheet("background-color: black;")

        self.__image_panel.setGeometry(0,0,self.__width, self.__height)
        self.__image_layer.raise_()
        
    def resizeEvent(self, event:QResizeEvent) -> None:
        size = event.size()
        self.__image_layer.setGeometry(0, 0, size.width(), size.height())
        self.__image_panel.setGeometry(0, 0, size.width(), size.height())
        self.__image_panel.resize_event()
        super().resizeEvent(event)
        
    def show(self) -> None:
        super().show()
        self.__image_panel.resize_event()
        
    def closeEvent(self, event:QCloseEvent) -> None:
        self.__image_layer.closeEvent(event)
        super().closeEvent(event)
        

# test code
def main():
    app = QApplication(sys.argv)
    main = Frame(100, 100, 500, 500)
    main.show()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    pass