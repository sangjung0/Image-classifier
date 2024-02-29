from multiprocessing import Queue, Value
import time

from video.buffer.Interface import Interface
from util.util import Loger, Timer
from util import TransceiverInterface
from project_constants import PROCESSOR_STOP, PROCESSOR_PAUSE

class Sender(Interface):
    def __init__(self, name:str, requiresSorting: bool = False, logerIsPrint: bool = False) -> None:
        super().__init__(requiresSorting)
        self.__logerIsPrint = logerIsPrint
        self.__name = name
        
    def __call__(self, order:int, terminationSignal:Value, flag:Value, outputQ:Queue, transceiver:TransceiverInterface) -> None: # type: ignore
        loger = Loger(self.__name, self.__logerIsPrint) # loger
        timer = Timer() # timer
        imgTimer = Timer() # timer
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
                        imgTimer.measure(lambda: data.compress())
                        loger("이미지 압축", option=imgTimer)
                        timer.measure(lambda :transceiver.send(outputQ, data))
                        loger("데이터 압축 후 송신", option=timer)
        except Exception as e:
            loger("쓰레드 오류",e, option="error") # loger
            flag.value = PROCESSOR_STOP
        loger("쓰레드 종료", option='terminate') # loger
        loger(f"압축 후 송신 평균 속도 {timer.average}", option='result')
        loger(f"이미지 압축 평균 속도 {imgTimer.average}", option='result')
        return

