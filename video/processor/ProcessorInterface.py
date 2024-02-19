from abc import ABC, abstractmethod
from multiprocessing import Queue, Value
import os
import time

from video.model.Section import Section
from util.transceiver import TransceiverInterface
from util.util import Timer, Loger, AllProcessIsTerminated
from project_constants import PROCESSOR_STOP, PROCESSOR_PAUSE

class ProcessorInterface(ABC):

    def __init__(self, name:str):
        self.__name = name

    @abstractmethod
    def __prepare__(self) -> None: pass
    
    @abstractmethod
    def processing(self, section: Section): pass

    def __call__(self, data: Queue, result: Queue, flag: Value, transceiver:TransceiverInterface, finish:AllProcessIsTerminated.allProcessIsTerminated): # type: ignore
        loger = Loger(self.__name) # logger
        try:
            self.__prepare__()

            timer = Timer() # timer
            loger(option="start") # loger
            while True:
                if flag.value == PROCESSOR_PAUSE:
                    time.sleep(0.1)
                elif flag.value == PROCESSOR_STOP:
                    break
                else:
                    if not data.empty():
                        timer.start() # timer
                        ret, data_ = transceiver.receive(data)
                        timer.end() # timer
                        loger("데이터 수신 후 압축 해제", option=timer) # loger
                        if ret:
                            timer.start() # timer
                            temp = self.processing(data_)
                            timer.end() # timer
                            loger(temp.index, "데이터 연산 완료", option=timer) # loger
                            timer.start() # timer
                            transceiver.send(result, temp)
                            timer.end() # timer
                            loger("데이터 압축 후 전송", option=timer) # loger
                        elif finish():
                            break
                    time.sleep(0.1)
            loger(os.getpid(), "연산 프로세서 종료", option="terminate")
        except Exception as e:
            loger(os.getpid(), "연산 프로세서 오류", e)
        return