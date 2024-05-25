import datetime
import pathlib
from PyQt5.QtWidgets import QWidget

from gui.imageLayer.interactiveObject.InteractiveObject import InteractiveObject


class ImageDataViewer(InteractiveObject):
    __X: int = 0
    __Y: int = 0
    __WIDTH: int = 200
    __HEIGHT: int = 100

    def __init__(self, base:QWidget, callback: callable, x: int = __X, y: int = __Y, width: int = __WIDTH, height: int = __HEIGHT, axes:tuple[int] = (0, 0)):
        super().__init__("",base, callback, x, y, width, height, axes)
        
        self.setStyleSheet("""
            QPushButton {
                background-color: lightgray;
                color: black;
                border: 1px solid black;
                border-radius: 5px;
                padding: 5px;
            }            
        """)
        
        self.set_data("test", datetime.datetime.now(), pathlib.Path("/image/"))
        

    def set_data(self, name: str, dt: datetime.datetime, path: pathlib.Path):
        self.setText(f"""
        name : {name}
        dt : {dt}
        path : {path}         
        """)
    
    