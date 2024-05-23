from program.gui.pathModal.PathModal import PathModal


class Init(PathModal):
    __SUCCESS_NAME: str = "start"

    def __init__(self, callback: callable):
        super().__init__(callback, Init.__SUCCESS_NAME)