from multiprocessing.sharedctypes import SynchronizedBase
from multiprocessing import Queue
import time

from program.core.scheduler.transceiver.Transceiver import Transceiver
from program.core.scheduler.dto import Converter
from core.scheduler.Constant import PROCESSOR_STOP, PROCESSOR_PAUSE

from utils import Loger, Timer

class Sender(Transceiver):
    def __init__(self, name:str, loger_is_print:bool=False) -> None:
        super().__init__()
        self.__name:str = name
        self.__loger_is_print:bool = loger_is_print

    def __call__(self, order: int, termination_signal: SynchronizedBase, flag: SynchronizedBase, queue: Queue):
        # --
        loger = Loger(self.__name, self.__loger_is_print)
        timer = Timer()
        loger("start", option="start")
        # --
        converter = Converter(queue)
        try:
            while True:
                if flag.value == PROCESSOR_STOP:
                    break
                elif flag.value == PROCESSOR_PAUSE:
                    time.sleep(0.1)
                else:
                    if self.empty():
                        if termination_signal.value >= order:
                            break
                        time.sleep(0.01)
                    else:
                        data = self.get()
                        timer.measure(lambda :converter.send(data))
                        loger("데이터 압축 후 송신", option=timer)
        except Exception as e:
            loger("쓰레드 오류",e, option="error") # loger
            flag.value = PROCESSOR_STOP
        loger(f"압축 후 송신 평균 속도 {timer.average}", option='result') # loger
        loger("쓰레드 종료", option='terminate') # loger
        return
