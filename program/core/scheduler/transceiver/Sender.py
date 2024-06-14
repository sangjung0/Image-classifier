from multiprocessing.sharedctypes import SynchronizedBase
from multiprocessing import Queue
import queue as EQ
import time

from core.scheduler.transceiver.Transceiver import Transceiver
from core.scheduler.dto import Converter
from core.Constant import PROCESSOR_STOP, PROCESSOR_PAUSE, MAX_BUF_SIZE

from utils import Loger, Timer

class Sender(Transceiver):
    """멀티 프로세싱에서 데이터를 송신하는 역할을 하는 클래스 """
    
    def __init__(self, name:str, loger_is_print:bool=False) -> None:
        super().__init__()
        self.__name:str = name
        self.__loger_is_print:bool = loger_is_print
        
    def is_full(self) -> bool:
        return len(self) == MAX_BUF_SIZE

    def __call__(self, order: int, termination_signal: SynchronizedBase, flag: SynchronizedBase, queue: Queue)->None:
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
                    if self.is_empty():
                        if termination_signal.value >= order:
                            break
                        time.sleep(0.01)
                    else:
                        data = self.get()
                        while flag.value != PROCESSOR_STOP:
                            try:
                                timer.measure(lambda: converter.send(data))
                            except EQ.Full:
                                continue
                            loger("데이터 압축 후 송신", option=timer)
                            break
        except Exception as e:
            loger("쓰레드 오류",e, option="error") # loger
            flag.value = PROCESSOR_STOP
        loger(f"압축 후 송신 평균 속도 {timer.average}", option='result') # loger
        loger("쓰레드 종료", option='terminate') # loger
