import datetime
import pathlib
from PyQt5.QtWidgets import QWidget

from gui.imageLayer.interactiveObject.InteractiveObject import InteractiveObject


class ImageDataViewer(InteractiveObject):
    __X_RATIO: int = 0
    __Y_RATIO: int = 0
    __WIDTH: int = 200
    __HEIGHT: int = 100

    def __init__(self, base:QWidget, callback: callable, x_ratio: float = __X_RATIO, y_ratio: float = __Y_RATIO, width: int = __WIDTH, height: int = __HEIGHT, axes:tuple[int] = (0, 0)):
        super().__init__("",base, callback, x_ratio, y_ratio, width, height, axes)
        self.set_data("test", datetime.datetime.now(), pathlib.Path("/image/"))
        

    def set_data(self, name: str, dt: datetime.datetime, path: pathlib.Path):
        self.setText(f"""
        name : {name}
        dt : {dt}
        path : {path}         
        """)
    
    