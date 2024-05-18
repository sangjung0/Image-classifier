from multiprocessing.sharedctypes import SynchronizedBase
from threading import Thread
from typing import Type

from image_data.buffer import Interface
from image_data.PathData import PathData
from image_data.processor import AllProcessIsTerminated, AllTransmissionMediumIsTerminated

from project_constants import PROCESSOR_PAUSE, PROCESSOR_RUN, PROCESSOR_STOP

class Loader:
    def __init__(self, data:PathData, buffer:Interface, bufferTh:Thread, flag: SynchronizedBase, processes: Type[AllProcessIsTerminated], mediums: Type[AllTransmissionMediumIsTerminated]) -> None:
        self.__data = data
        self.__buffer = buffer
        self.__bufferTh = bufferTh
        self.__flag = flag
        self.__processes = processes
        self.__mediums = mediums
        self.__iter = iter([])

    @property
    def data(self) -> PathData:
        return self.__data
    
    def isFinish(self) -> bool:
        if self.__flag.value == PROCESSOR_STOP or self.__processes.allProcessIsTerminated() or not self.__bufferTh.is_alive():
            return True
        return False

    def pause(self) -> None:
        self.__flag.value = PROCESSOR_PAUSE

    def stop(self) -> None:
        self.__flag.value = PROCESSOR_STOP
        self.__processes.wait()
        self.__mediums.wait()

    def run(self) -> None:
        if self.__flag.value != PROCESSOR_STOP:
            self.__flag.value = PROCESSOR_RUN
        else: raise Exception("프로세서 종료됨")

    def __iter__(self):
        return self
    
    def __next__(self) -> tuple[int, bool, object]:
        try:
            data = next(self.__iter)
            return PROCESSOR_RUN, True, data
        except StopIteration:
            section = self.__buffer.get()
            if section is None:
                if self.isFinish():
                    raise StopIteration
                return PROCESSOR_RUN, False, None
            self.__iter = iter(section)
            return self.__next__()
        
class SingleLoader:
    def __init__(self, data:PathData, process:object):
        self.__data = data
        self.__process = process
        self.__iter = iter([])

    @property
    def videoData(self):
        return self.__data
    
    def run(self):
        return
    
    def stop(self):
        return 
    
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            data = next(self.__iter)
            return PROCESSOR_RUN, True, data
        except StopIteration:
            section = self.__process.get()
            if section is None: raise StopIteration
            self.__iter = iter(section)
            return self.__next__()