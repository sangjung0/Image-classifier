from multiprocessing import Value
from typing import Type

from video.buffer import Interface
from video.VideoData import VideoData
from util.util import AllProcessIsTerminated, AllTransmissionMediumIsTerminated
from project_constants import PROCESSOR_PAUSE, PROCESSOR_RUN, PROCESSOR_STOP

class Loader:
    def __init__(self, data:VideoData, buffer:Interface, flag: Value, processes: Type[AllProcessIsTerminated], mediums: Type[AllTransmissionMediumIsTerminated]): # type: ignore
        self.__data = data
        self.__buffer = buffer
        self.__flag = flag
        self.__processes = processes
        self.__mediums = mediums
        self.__iter = iter([])
        self.__index = 0

    @property
    def videoData(self):
        return self.__data
    
    def isFinish(self):
        if self.__flag.value == PROCESSOR_STOP or self.__processes.allProcessIsTerminated():
            return True
        return False

    def pause(self):
        self.__flag.value = PROCESSOR_PAUSE

    def stop(self):
        self.__flag.value = PROCESSOR_STOP
        self.__processes.wait()
        self.__mediums.wait()

    def run(self):
        if self.__flag.value != PROCESSOR_STOP:
            self.__flag.value = PROCESSOR_RUN
        else: raise Exception("프로세서 종료됨")

    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            frame = next(self.__iter)
            return PROCESSOR_RUN, True, frame
        except StopIteration:
            section = self.__buffer.get(self.__index)
            if section is None:
                if self.__flag ==  PROCESSOR_STOP:
                    raise StopIteration
                return PROCESSOR_RUN, False, None
            self.__iter = iter(section)
            self.__index += 1
            return self.__next__()
        
class SingleLoader:
    def __init__(self, videoData:VideoData, process:object):
        self.__data = videoData
        self.__process = process
        self.__iter = iter([])

    @property
    def videoData(self):
        return self.__data
    
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            frame = next(self.__iter)
            return PROCESSOR_RUN, True, frame
        except StopIteration:
            section = self.__process.get()
            self.__iter = iter(section)
            return self.__next__()