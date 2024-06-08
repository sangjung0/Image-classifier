from PyQt5.QtWidgets import QWidget

from gui.imageLayer.interactiveObject.InteractiveObject import InteractiveObject
from gui.Constant import AUTO_ORGANIZATION_NAME, AUTO_ORGANIZATION_WIDTH, AUTO_ORGANIZATION_HEIGHT, AUTO_ORGANIZATION_X_RATIO, AUTO_ORGANIZATION_Y_RATIO


class AutoSave(InteractiveObject):

    def __init__(self, 
                 base:QWidget, 
                 callback: callable, 
                 x_ratio: float = AUTO_ORGANIZATION_X_RATIO, 
                 y_ratio: float = AUTO_ORGANIZATION_Y_RATIO, 
                 width: int = AUTO_ORGANIZATION_WIDTH, 
                 height: int = AUTO_ORGANIZATION_HEIGHT, 
                 axes: tuple[int] = (0, 0)
                 ) -> None:
        super().__init__(AUTO_ORGANIZATION_NAME, base, callback, x_ratio, y_ratio, width, height, axes)
        
        self.setStyleSheet("background-color: rgba(0, 0, 0, 10); border: none; color: white; font-size:18px; border-radius:15px;")
        