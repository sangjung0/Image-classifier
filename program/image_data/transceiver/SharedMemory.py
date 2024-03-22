from multiprocessing.shared_memory import SharedMemory as SM
import numpy as np
import time

from image_data.transceiver.Interface import Interface

from image_data.model import Section, Image
from project_constants import CHARACTER_SIZE

class SharedMemory(Interface):
    MAX_LOOP = 100

    def __init__(self, batchSize:int, memory:SM, prevKey:int, key:int, nextKey:int, size:tuple[int, int], dtype=np.uint8):
        
        self.size = size
        self.__imgSizeStart = 1 + CHARACTER_SIZE
        self.__key = key
        self.__prevKey = prevKey
        self.__nextKey = nextKey
        self.__batchSize = batchSize
        self.__index = 0
        self.__sectionIdx = 0

        self.memory = np.ndarray(size, dtype=dtype, buffer=memory)

    def send(self, index:int) -> None:
        self.memory[index][0] = self.__nextKey

    def receive(self) -> tuple[bool, Section]:
        l = SharedMemory.MAX_LOOP
        section = Section(self.__sectionIdx)
        self.__sectionIdx += 1

        while(l>0 and len(section) < self.__batchSize):
            if self.memory[self.__index, 0] == self.__prevKey:
                self.memory[self.__index, 0] = self.__key
                if self.memory[self.__index, 0] == self.__key: # 이 과정이 필요할까?
                    section.append(Image(self.__index, self.memory[self.__index, self.__imgSizeStart:]))
            else:
                l -= 1
                time.sleep(0.01)
            self.__index += 1

        if len(section) > 0:
            return True, section
        return False, None