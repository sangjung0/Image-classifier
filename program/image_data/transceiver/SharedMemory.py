from multiprocessing.shared_memory import SharedMemory as SM
import numpy as np

from image_data.transceiver.Interface import Interface

class SharedMemory(Interface):
    def __init__(self, imageMemory:SM, imageNumberMemory:SM, keyMemory:SM, prevKey:int,
                 key:int, nextKey:int, size:tuple[int, int, int, int, int], dtype=np.uint8,):
        
        self.size = size
        self.__key = key
        self.__prevKey = prevKey
        self.__nextKey = nextKey
        self.__index = 0

        self.imageMemory = np.ndarray(size, dtype=dtype, buffer=imageMemory)
        self.imageNumberMemory = np.ndarray(size[0:2], dtype=dtype, buffer=imageNumberMemory)
        self.keyMemory = np.ndarray(size[0:1], dtype=dtype, buffer=keyMemory)


    def send(self, index:int) -> None:
        self.keyMemory[index] = self.__nextKey

    def receive(self):
        if self.keyMemory[self.__index] == self.__prevKey:
            self.keyMemory[self.__index] = self.__key
            if self.keyMemory[self.__index] == self.key:
                return zip(self.imageNumberMemory[self.__index], self.imageMemory[self.__index])
        self.__index += 1