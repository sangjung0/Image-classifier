from PyQt5.QtWidgets import QWidget

from gui.imageLayer.interactiveObject.InteractiveObject import InteractiveObject
from gui.Constant import NEW_FOLDER_HEIGHT, NEW_FOLDER_NAME, NEW_FOLDER_AXES, NEW_FOLDER_WIDTH, NEW_FOLDER_X_RATIO, NEW_FOLDER_Y_RATIO

class NewFolder(InteractiveObject):

    def __init__(self, 
                 base:QWidget, 
                 callback: callable, 
                 x_ratio: float = NEW_FOLDER_X_RATIO, 
                 y_ratio: float = NEW_FOLDER_Y_RATIO, 
                 width: int = NEW_FOLDER_WIDTH, 
                 height: int = NEW_FOLDER_HEIGHT, 
                 axes:tuple[int] = NEW_FOLDER_AXES
                 ) -> None:
        super().__init__(NEW_FOLDER_NAME, base, callback, x_ratio, y_ratio, width, height, axes)
        
        self.setStyleSheet("background-color: rgba(0, 0, 0, 10); border: none; color: white; font-size:18px; border-radius:15px;")
        
