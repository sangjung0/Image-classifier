from multiprocessing import Queue, Value
from threading import Lock
import bisect
import time

from util.transceiver import TransceiverInterface
from video.model import VideoSection
from project_constants import STOP, PAUSE, RUN
class VideoBuffer:
    def __init__(self):
        self.__videoSections = []
        self.__lock = Lock()

    def append(self, value:VideoSection):
        with self.__lock:
            bisect.insort(self.__videoSections, value)

    def get(self, index):
        with self.__lock:
            if len(self.__videoSections) > 0 and self.__videoSections[0].index == index:
                return self.__videoSections.pop(0)
            return None
    
    def __call__(self, result:Queue, flag:Value, finish, transceiver:TransceiverInterface): # type: ignore
        try:
            while True:
                if flag.value == STOP:
                    break
                elif flag.value == PAUSE:
                    time.sleep(0.1)
                else:
                    ret, data = transceiver.receive(result)
                    if ret:
                        self.append(data)
                        print("버퍼에 담김")
                    elif finish():
                        flag.value = STOP
        except Exception as e:
            print("버퍼 쓰레드 오류", e)
        print("버퍼 쓰레드 종료")
        return
