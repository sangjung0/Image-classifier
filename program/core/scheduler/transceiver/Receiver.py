from multiprocessing.sharedctypes import SynchronizedBase
from multiprocessing import Queue
import queue as EQ
import time

from core.scheduler.transceiver.Transceiver import Transceiver
from core.scheduler.dto import Converter
from core.Constant import PROCESSOR_STOP, PROCESSOR_PAUSE, MAX_BUF_SIZE

from utils import Loger, Timer


class Receiver(Transceiver):
    """멀티 프로세싱에서 데이터를 수신받는 역할을 하는 클래스"""
    
    def __init__(self, name:str, loger_is_print:bool=False) -> None:
        super().__init__()
        self.__name:str = name
        self.__loger_is_print:bool = loger_is_print
        
    def __is_full(self) -> bool:
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
                elif self.__is_full():
                    time.sleep(0.1)
                else:
                    try:
                        ret, data = timer.measure(lambda : converter.receive())
                        loger("데이터 수신 후 압축 해제", option=timer)
                        if ret: 
                            self.append(data)
                    except EQ.Empty:
                        if termination_signal.value >= order:
                            break
        except Exception as e:
            loger("쓰레드 오류",e, option="error") # loger
            flag.value = PROCESSOR_STOP
        loger(f"데이서 수신 후 압축 해제 평균 속도 {timer.average}", option='result') # loger
        loger("쓰레드 종료", option='terminate') # loger


