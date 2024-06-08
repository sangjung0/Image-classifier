from PyQt5.QtWidgets import QWidget

from gui.pathModal.PathModal import PathModal
from gui.Constant import ADD_PATH_CONFIRM_NAME, ADD_PATH_CANCEL_NAME


class AddPath(PathModal):
    __CONFIRM_NAME: str = ADD_PATH_CONFIRM_NAME
    __CANCEL_NAME: str = ADD_PATH_CANCEL_NAME

    def __init__(self, base:QWidget, callback: callable) -> None:
        """
        base -- QWidget 모달 종속 위젯
        callback -- callable 성공시 실행 함수
        """
        super().__init__(base, callback, AddPath.__CONFIRM_NAME, AddPath.__CANCEL_NAME)