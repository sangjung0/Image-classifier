from PyQt5.QtWidgets import QWidget

from gui.imageLayer.interactiveObject.InteractiveObject import InteractiveObject


class Next(InteractiveObject):
    __NAME:str = "Next"
    __X_RATIO: float = 0
    __Y_RATIO: float = 0
    __WIDTH: int = 200
    __HEIGHT: int = 60

    def __init__(self, base: QWidget, callback: callable, x_ratio: float = __X_RATIO, y_ratio: float = __Y_RATIO, width: int = __WIDTH, height: int = __HEIGHT, axes:tuple[int] = (0, 0)) -> None:
        super().__init__(Next.__NAME, base, callback, x_ratio, y_ratio, width, height, axes)
