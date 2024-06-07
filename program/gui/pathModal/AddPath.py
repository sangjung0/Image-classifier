from PyQt5.QtWidgets import QWidget

from gui.pathModal.PathModal import PathModal


class AddPath(PathModal):
    __CONFIRM_NAME: str = "Add"
    __CANCEL_NAME: str = "Cancel"

    def __init__(self, base:QWidget, callback: callable) -> None:
        """
        base -- QWidget 모달 종속 위젯
        callback -- callable 성공시 실행 함수
        """
        super().__init__(base, callback, AddPath.__CONFIRM_NAME, AddPath.__CANCEL_NAME)