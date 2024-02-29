from threading import Lock
import bisect

class Interface:
    def __init__(self, requiresSorting:bool = False) -> None:
        self._datas = []
        self.__lock = Lock()
        self.__append = self.__sortAppend if requiresSorting else self.__unSortAppend

    def __sortAppend(self, value:object) -> None:
        bisect.insort(self._datas, value)
    
    def __unSortAppend(self, value:object) -> None:
        self._datas.append(value)

    def append(self, value:object) -> None:
        with self.__lock:
            self.__append(value)

    def get(self, index = None) -> object:
        with self.__lock:
            if not self.empty() and (index == None or self._datas[0].index == index):
                return self._datas.pop(0)
            return None
    
    def empty(self)->bool:
        return len(self._datas) == 0
    

