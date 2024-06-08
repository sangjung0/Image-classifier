from PyQt5.QtWidgets import QWidget

from gui.imageLayer.interactiveObject.InteractiveObject import InteractiveObject


class Prev(InteractiveObject):
    __NAME: str = "<<<"
    __X_RATIO: int = 0
    __Y_RATIO: int = 0
    __WIDTH: int = 200
    __HEIGHT: int = 60

    def __init__(self, base:QWidget, callback: callable, x_ratio: float = __X_RATIO, y_ratio: float = __Y_RATIO, width: int = __WIDTH, height: int = __HEIGHT, axes: tuple[int] = (0, 0)) -> None:
        super().__init__(Prev.__NAME, base, callback, x_ratio, y_ratio, width, height, axes)
        
        self.setStyleSheet("background-color: rgba(0, 0, 0, 10); border: none; color: white; font-size:24px; border-radius:15px;")