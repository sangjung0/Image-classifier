from program.gui.Frame import Frame


class MainFrame(Frame):
    __X: int = 0
    __Y: int = 0
    __WIDTH: int = 500
    __HEIGHT: int = 500

    def __init__(self, x: int = __X, y: int = __Y, width: int = __WIDTH, height: int = __HEIGHT):
        super().__init__(x, y, width, height)

    def __path_event(self):
        pass