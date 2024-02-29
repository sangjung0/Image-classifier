from threading import Lock
import bisect

from video.model import Section

class Interface:
    def __init__(self, requiresSorting:bool = False) -> None:
        self._datas = []
        self.__lock = Lock()
        self.__append = self.__sortAppend if requiresSorting else self.__unSortAppend

    def __sortAppend(self, value:Section) -> None:
        bisect.insort(self._datas, value)
    
    def __unSortAppend(self, value:Section) -> None:
        self._datas.append(value)

    def append(self, value:Section) -> None:
        with self.__lock:
            self.__append(value)

    def get(self, index = None) -> Section:
        with self.__lock:
            if not self.empty() and (index == None or self._datas[0].index == index):
                return self._datas.pop(0)
            return None
    
    def empty(self)->bool:
        return len(self._datas) == 0
    

