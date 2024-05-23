import datetime
import pathlib

from program.gui.imageLayer.interactiveObject.InteractiveObject import InteractiveObject


class ImageDataViewer(InteractiveObject):
    __X: int = 0
    __Y: int = 0
    __WIDTH: int = 200
    __HEIGHT: int = 100

    def __init__(self, callback: callable, x: int = __X, y: int = __Y, width: int = __WIDTH, height: int = __HEIGHT):
        super().__init__(callback, x, y, width, height)

    def set_data(self, name: str, dt: datetime.datetime, path: pathlib.Path):
        pass