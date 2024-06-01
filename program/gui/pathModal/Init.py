
from gui.pathModal.PathModal import PathModal


class Init(PathModal):
    __CONFIRM_NAME: str = "Start"
    __CANCEL_NAME: str = "Exit"
    

    def __init__(self, callback: callable):
        """
        base -- QWidget 모달 종속 위젯
        callback -- callable 성공시 실행 함수
        """
        super().__init__(None, callback, Init.__CONFIRM_NAME, Init.__CANCEL_NAME)