from multiprocessing.shared_memory import SharedMemory as SM
from pathlib import Path
import numpy as np
import time

from image_data.transceiver.Interface import Interface

from image_data.model import Section, Image
from project_constants import CHARACTER_SIZE, ORDER_SIZE, PHASE_SIZE, SCALE_SIZE

class SharedMemory(Interface):
    MAX_LOOP = 100

    def __init__(self, memory:SM, size:tuple[int, int], dataSize:tuple, batchSize:int, prevKey:int, key:int, nextKey:int, dataDType=np.uint8):
        
        self.memory = np.ndarray(size, dtype=np.byte, buffer=memory.get_obj())
        self.__size = size[0]
        self.__dataSize = dataSize
        self.__batchSize = batchSize
        self.__prevKey = np.frombuffer(prevKey.to_bytes(PHASE_SIZE), dtype=np.byte)
        self.__key = np.frombuffer(key.to_bytes(PHASE_SIZE), dtype=np.byte)
        self.__nextKey = np.frombuffer(nextKey.to_bytes(PHASE_SIZE), dtype=np.byte)
        self.__dataDType = dataDType

        self.__imgSizeStart = PHASE_SIZE + ORDER_SIZE + SCALE_SIZE + CHARACTER_SIZE
        self.__characterStart = PHASE_SIZE + ORDER_SIZE + SCALE_SIZE
        self.__scaleStart = PHASE_SIZE + ORDER_SIZE
        self.__index = 0
        self.__sectionIdx = 0


    def send(self, section:Section) -> None:
        for img, index in zip(section.data, section.dataIndex):
            self.memory[index, PHASE_SIZE:self.__scaleStart] = np.frombuffer(img.index.to_bytes(ORDER_SIZE), dtype=np.byte)
            self.memory[index, self.__scaleStart: self.__characterStart] = np.frombuffer(img.getScale().to_bytes(SCALE_SIZE), dtype=np.byte)
            string = np.frombuffer(str(img.path).encode(), dtype=np.byte)
            self.memory[index, self.__characterStart:self.__characterStart+string.shape[0]] =string 
            self.memory[index, 0:PHASE_SIZE] = self.__nextKey

    def receive(self) -> tuple[bool, Section]:
        l = SharedMemory.MAX_LOOP
        section = Section(self.__sectionIdx)
        self.__sectionIdx += 1

        while(l>0 and len(section) < self.__batchSize):
            if self.memory[self.__index, :PHASE_SIZE] == self.__prevKey:
                self.memory[self.__index, :PHASE_SIZE] = self.__key
                if self.memory[self.__index, :PHASE_SIZE] == self.__key: # 이 과정이 필요할까?
                    l = SharedMemory.MAX_LOOP
                    section.append(
                        Image(
                            int.from_bytes(self.memory[self.__index, PHASE_SIZE: self.__scaleStart].tobytes()),
                            int.from_bytes(self.memory[self.__index, self.__scaleStart: self.__characterStart].tobytes()),
                            Path(self.memory[self.__index, self.__characterStart:self.__imgSizeStart].tobytes().decode("utf-8")),
                            np.ndarray(self.__dataSize, dtype=self.__dataDType, buffer=self.memory[self.__index, self.__imgSizeStart:])
                            ),
                        self.__index, 
                    )
            else:
                l -= 1
                time.sleep(0.01)
            self.__index = (self.__index + 1) % self.__size

        if len(section) > 0:
            return True, section
        return False, None