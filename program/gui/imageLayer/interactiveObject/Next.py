from PyQt5.QtWidgets import QWidget

from gui.imageLayer.interactiveObject.InteractiveObject import InteractiveObject
from gui.Constant import NEXT_HEIGHT, NEXT_NAME, NEXT_WIDTH, NEXT_X_RATIO, NEXT_Y_RATIO, NEXT_AXES

class Next(InteractiveObject):

    def __init__(self, 
                 base: QWidget, 
                 callback: callable, 
                 x_ratio: float = NEXT_X_RATIO, 
                 y_ratio: float = NEXT_Y_RATIO, 
                 width: int = NEXT_WIDTH, 
                 height: int = NEXT_HEIGHT, 
                 axes:tuple[int] = NEXT_AXES
                 ) -> None:
        super().__init__(NEXT_NAME, base, callback, x_ratio, y_ratio, width, height, axes)
    
        self.setStyleSheet("background-color: rgba(0, 0, 0, 10); border: none; color: white; font-size:24px; border-radius:15px;")