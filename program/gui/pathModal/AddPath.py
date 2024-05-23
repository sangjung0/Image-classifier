from program.gui.pathModal.PathModal import PathModal


class AddPath(PathModal):
    __SUCCESS_NAME: str = "add"

    def __init__(self, callback: callable):
        super().__init__(callback, AddPath.__SUCCESS_NAME)