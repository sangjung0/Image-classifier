from PyQt5.QtCore import QPoint

from gui.pathModal.PathModal import PathModal


class AddPath(PathModal):
    __CONFIRM_NAME: str = "Add"
    __CANCEL_NAME: str = "Cancel"

    def __init__(self, center:QPoint, success_callback: callable, cancel_callback: callable):
        """
        center -- QPoint 모달 center 위치
        confirm_callback -- callable 성공시 실행 함수
        cancel_callback -- callable 실패시 실행 함수
        """
        super().__init__(center, success_callback, cancel_callback, AddPath.__CONFIRM_NAME, AddPath.__CANCEL_NAME)