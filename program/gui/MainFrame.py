import sys
import pathlib
from PyQt5.QtWidgets import QApplication, QDesktopWidget

from gui.imageLayer import MainImageLayer
from gui.Frame import Frame
from gui.pathModal import Init

from core import MainDataController

class MainFrame(Frame):
    """
    메인 GUI
    """
    __X: int = 0
    __Y: int = 0
    __WIDTH: int = 500
    __HEIGHT: int = 500

    def __init__(self, x: int = __X, y: int = __Y, width: int = __WIDTH, height: int = __HEIGHT):
        center = QDesktopWidget().availableGeometry().center()
        super().__init__(center.x(), center.y(), width, height)
    
        self.init = Init(center, self.__path_event, self.__exit)
        self.init.show()
        
    def __path_event(self, path:pathlib.Path):
        self.set_image_layer(MainDataController(path),MainImageLayer)
        self.show()
        
    def __exit(self):
        self.close()
    
    
# test code
def main():
    app = QApplication(sys.argv)
    main = MainFrame(100, 100, 500, 500)
    sys.exit(app.exec())
    
if __name__ == "__main__":
    pass