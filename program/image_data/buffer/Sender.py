from multiprocessing.sharedctypes import SynchronizedBase 
import time

from image_data.buffer.Interface import Interface

from image_data.transceiver import Interface as TI

from project_constants import PROCESSOR_STOP, PROCESSOR_PAUSE

from util.util import Loger, Timer

class Sender(Interface):
    def __init__(self, name:str, requiresSorting: bool = False, logerIsPrint: bool = False) -> None:
        super().__init__(requiresSorting)
        self.__logerIsPrint = logerIsPrint
        self.__name = name
        
    def __call__(self, order:int, terminationSignal:SynchronizedBase, flag:SynchronizedBase, transceiver:TI) -> None: # type: ignore
        loger = Loger(self.__name, self.__logerIsPrint) # loger
        timer = Timer() # timer
        loger("start", option="start") # loger
        try:
            while True:
                if flag.value == PROCESSOR_STOP:
                    break
                elif flag.value == PROCESSOR_PAUSE:
                    time.sleep(0.1)
                else:
                    if self.empty():
                        if terminationSignal.value >= order:
                            break
                        time.sleep(0.01)
                    else:
                        data = self.get()
                        timer.measure(lambda :transceiver.send(data))
                        loger("데이터 압축 후 송신", option=timer)
        except Exception as e:
            loger("쓰레드 오류",e, option="error") # loger
            flag.value = PROCESSOR_STOP
        loger(f"압축 후 송신 평균 속도 {timer.average}", option='result') # loger
        loger("쓰레드 종료", option='terminate') # loger
        return

