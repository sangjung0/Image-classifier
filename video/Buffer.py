from multiprocessing import Queue, Value
from threading import Lock
import bisect
import time

from util.transceiver import TransceiverInterface
from video.model import Section
from project_constants import PROCESSOR_STOP, PROCESSOR_PAUSE
from util.util import Loger, Timer

class Buffer:
    def __init__(self):
        self.__videoSections = []
        self.__lock = Lock()

    def append(self, value:Section):
        with self.__lock:
            bisect.insort(self.__videoSections, value)

    def get(self, index):
        with self.__lock:
            if len(self.__videoSections) > 0 and self.__videoSections[0].index == index:
                return self.__videoSections.pop(0)
            return None
    
    def __call__(self, result:Queue, flag:Value, finish, transceiver:TransceiverInterface): # type: ignore
        loger = Loger("VideoBuffer") # loger
        try:
            timer = Timer() # timer
            loger(option="start") # loger
            while True:
                if flag.value == PROCESSOR_STOP:
                    break
                elif flag.value == PROCESSOR_PAUSE:
                    time.sleep(0.1)
                else:
                    if not result.empty():
                        timer.start()
                        ret, data = transceiver.receive(result)
                        timer.end()
                        loger("데이터 수신 후 압축 해제", option=timer)
                        if ret:
                            timer.start() # timer
                            self.append(data)
                            timer.end() # timer
                            loger("버퍼에 담김", option=timer) # loger
                        elif finish():
                            flag.value = PROCESSOR_STOP
        except Exception as e:
            loger("버퍼 쓰레드 오류",e) # loger
        loger("버퍼 쓰레드 종료", option='terminate') # loger
        return
