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

    def __init__(self, path:pathlib.Path, x: int = __X, y: int = __Y, width: int = __WIDTH, height: int = __HEIGHT):
        super().__init__(x, y, width, height, MainImageLayer, MainDataController(path))
        
        
    @staticmethod
    def start():
        app = QApplication(sys.argv)
        x:pathlib.Path = None
        def path_event(path:pathlib.Path):
            nonlocal x
            x = path
        init = Init(path_event)
        center = QDesktopWidget().availableGeometry().center()
        init.show(center)
        init.exec_()
        
        if x is not None:
            main = MainFrame(x, center.x(), center.y())
            main.show()
            try:
                sys.exit(app.exec())
            except Exception as _:
                main.close()
    
if __name__ == "__main__":
    pass