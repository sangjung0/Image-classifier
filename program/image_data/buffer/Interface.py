from threading import Lock
import bisect

from image_data.model import Section

class Interface:
    def __init__(self, requiresSorting:bool = False) -> None:
        self.__datas = []
        self.__lock = Lock()
        self.__index = 0

        self.__append = self.__sortAppend if requiresSorting else self.__unSortAppend
        self.__get = self.__sortGet if requiresSorting else self.__unSortGet

    def __sortAppend(self, value:Section) -> None:
        bisect.insort(self.__datas, value)
    
    def __unSortAppend(self, value:Section) -> None:
        self.__datas.append(value)

    def __sortGet(self) -> Section:
        if self.__datas[0].index == self.__index:
            self.__index += 1
            return self.__datas.pop(0)
        return None
        
    def __unSortGet(self) -> Section:
        return self.__datas.pop(0)
    
    def __len__(self) -> int:
        return len(self.__datas)

    def append(self, value:Section) -> None:
        with self.__lock:
            self.__append(value)

    def get(self) -> Section:
        with self.__lock:
            if not self.empty(): return self.__get()
        return None
    
    def empty(self)->bool:
        return len(self.__datas) == 0
    

