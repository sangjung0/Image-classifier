from gui.pathModal.PathModal import PathModal
from gui.Constant import INIT_CANCEL_NAME, INIT_CONFIRM_NAME

class Init(PathModal):
    __CONFIRM_NAME: str = INIT_CONFIRM_NAME
    __CANCEL_NAME: str = INIT_CANCEL_NAME
    

    def __init__(self, callback: callable):
        """
        base -- QWidget 모달 종속 위젯
        callback -- callable 성공시 실행 함수
        """
        super().__init__(None, callback, Init.__CONFIRM_NAME, Init.__CANCEL_NAME)