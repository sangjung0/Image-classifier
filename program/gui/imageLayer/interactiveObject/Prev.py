from PyQt5.QtWidgets import QWidget

from gui.imageLayer.interactiveObject.InteractiveObject import InteractiveObject
from gui.Constant import PREV_HEIGHT, PREV_NAME, PREV_WIDTH, PREV_X_RATIO, PREV_Y_RATIO, PREV_AXES

class Prev(InteractiveObject):

    def __init__(self, 
                 base:QWidget, 
                 callback: callable, 
                 x_ratio: float = PREV_X_RATIO, 
                 y_ratio: float = PREV_Y_RATIO, 
                 width: int = PREV_WIDTH, 
                 height: int = PREV_HEIGHT, 
                 axes: tuple[int] = PREV_AXES
                 ) -> None:
        super().__init__(PREV_NAME, base, callback, x_ratio, y_ratio, width, height, axes)
        
        self.setStyleSheet("background-color: rgba(0, 0, 0, 10); border: none; color: white; font-size:24px; border-radius:15px;")