import sys
import pathlib
from PyQt5.QtWidgets import QApplication, QDesktopWidget

from gui.imageLayer import MainImageLayer
from gui.Frame import Frame
from gui.pathModal import Init

from core import MainDataController
from gui.Constant import MAIN_FRAME_HEIGHT, MAIN_FRAME_WIDTH, MAIN_FRAME_X, MAIN_FRAME_Y

class MainFrame(Frame):
    """
    메인 GUI
    """

    def __init__(self, 
                 path:pathlib.Path,
                 x: int = MAIN_FRAME_X, 
                 y: int = MAIN_FRAME_Y, 
                 width: int = MAIN_FRAME_WIDTH, 
                 height: int = MAIN_FRAME_HEIGHT
                 ) -> None:
        super().__init__(x, y, width, height, MainImageLayer, MainDataController(path))
        
        
    @staticmethod
    def start() -> None:
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