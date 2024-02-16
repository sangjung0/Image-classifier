from video.VideoSection import VideoSection
from multiprocessing import Queue, Value
from project_constants import STOP, PAUSE, RUN
from threading import Lock
import pickle
import bisect
import time
class VideoBuffer:
    def __init__(self):
        self.__ary = []
        self.__lock = Lock()

    def append(self, value:VideoSection):
        with self.__lock:
            bisect.insort(self.__ary, value)
    
    def get(self, index):
        with self.__lock:
            if len(self.__ary) == 0:
                raise Exception("비었읍")
            if self.__ary[0].index != index:
                raise Exception("아직 안됨")
            return self.__ary.pop(0)
    
    def __call__(self, result:Queue, flag:Value, finish): # type: ignore
        while True:
            #time.sleep(1)
            if flag.value == STOP:
                break
            else:
                if not result.empty():
                    print("버퍼에 담김")
                    self.append(pickle.loads(result.get()))
                elif finish():
                    flag.value = STOP
        print("버퍼 프로세서 종료")
