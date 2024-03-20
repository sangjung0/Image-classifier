from multiprocessing import Queue, Value
import time

from image_data.buffer.Interface import Interface

from image_data.transceiver import TransceiverInterface

from project_constants import PROCESSOR_STOP, PROCESSOR_PAUSE

from util.util import Loger, Timer

class Receiver(Interface):
    def __init__(self, name:str, bufSize: int, requiresSorting: bool = False, logerIsPrint: bool = False) -> None:
        super().__init__(requiresSorting)
        self.__bufSize = bufSize
        self.__logerIsPrint = logerIsPrint
        self.__name = name

    def isFull(self) -> bool:
        return len(self) == self.__bufSize

    def __call__(self, order:int, terminationSignal:Value, flag:Value, inputQ:Queue, transceiver:TransceiverInterface) -> None: # type: ignore
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
                    if inputQ.empty():
                        if terminationSignal.value >= order:
                            break
                        time.sleep(0.01)
                    elif self.isFull():
                        time.sleep(0.01)
                    else:
                        ret, data = timer.measure(lambda :transceiver.receive(inputQ))
                        loger("데이터 수신 후 압축 해제", option=timer)
                        if ret: 
                            imgTimer.measure(lambda: data.deCompress())
                            self.append(data)
        except Exception as e:
            loger("쓰레드 오류",e, option="error") # loger
            flag.value = PROCESSOR_STOP
        loger(f"데이서 수신 후 압축 해제 평균 속도 {timer.average}", option='result') # loger
        loger(f"이미지 압축 해제 평균 속도 {imgTimer.average}", option='result') # loger
        loger("쓰레드 종료", option='terminate') # loger
        return

