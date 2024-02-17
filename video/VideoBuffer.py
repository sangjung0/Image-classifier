from video.model import VideoSection
from multiprocessing import Queue, Value
from project_constants import STOP, PAUSE, RUN
from threading import Lock
import pickle
import bisect
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
    
    def __call__(self, result:Queue, flag:Value, finish): # type: ignore
        while True:
            if flag.value == STOP:
                break
            else:
                if not result.empty():
                    print("버퍼에 담김")
                    self.append(pickle.loads(result.get()))
                elif finish():
                    flag.value = STOP
        print("버퍼 쓰레드 종료")
