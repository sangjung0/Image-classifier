from program.gui.imageLayer.interactiveObject.InteractiveObject import InteractiveObject


class Prev(InteractiveObject):
    __X: int = 0
    __Y: int = 0
    __WIDTH: int = 200
    __HEIGHT: int = 60

    def __init__(self, callback: callable, x: int = __X, y: int = __Y, width: int = __WIDTH, height: int = __HEIGHT):
        super().__init__(callback, x, y, width, height)
