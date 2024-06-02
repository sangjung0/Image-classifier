from PyQt5.QtWidgets import QWidget

from gui.imageLayer.interactiveObject.InteractiveObject import InteractiveObject


class Prev(InteractiveObject):
    __X_RATIO: int = 0
    __Y_RATIO: int = 0
    __WIDTH: int = 200
    __HEIGHT: int = 60

    def __init__(self, base:QWidget, callback: callable, x_ratio: float = __X_RATIO, y_ratio: float = __Y_RATIO, width: int = __WIDTH, height: int = __HEIGHT, axes: tuple[int] = (0, 0)):
        super().__init__("Prev", base, callback, x_ratio, y_ratio, width, height, axes)
        
        self.setStyleSheet("""
            QPushButton {
                background-color: lightgray;
                color: black;
                border: 1px solid black;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:pressed {
                background-color: gray;
            }            
        """)
