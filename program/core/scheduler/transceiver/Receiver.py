from multiprocessing.sharedctypes import SynchronizedBase
from multiprocessing import Queue
import time

from core.scheduler.transceiver.Transceiver import Transceiver
from core.scheduler.dto import Converter
from core.scheduler.Constant import PROCESSOR_STOP, PROCESSOR_PAUSE

from utils import Loger, Timer


class Receiver(Transceiver):
    def __init__(self, name:str, buf_size:int, loger_is_print:bool=False) -> None:
        super().__init__()
        self.__name:str = name
        self.__buf_size:int = buf_size
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
                    if queue.empty():
                        if termination_signal.value >= order:
                            break
                        time.sleep(0.01)
                    elif self.is_full():
                        time.sleep(0.01)
                    else:
                        ret, data = timer.measure(lambda : converter.receive())
                        loger("데이터 수신 후 압축 해제", option=timer)
                        if ret: 
                            self.append(data)
        except Exception as e:
            loger("쓰레드 오류",e, option="error") # loger
            flag.value = PROCESSOR_STOP
        loger(f"데이서 수신 후 압축 해제 평균 속도 {timer.average}", option='result') # loger
        loger("쓰레드 종료", option='terminate') # loger
        return

    def is_full(self) -> bool:
        return len(self) == self.__buf_size

