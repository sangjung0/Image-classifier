from abc import ABC, abstractmethod
from multiprocessing import Queue, Value
from threading import Thread, Lock
import os
import time

from video.model.Section import Section
from util.transceiver import TransceiverInterface
from util.util import Timer, Loger, AllProcessIsTerminated
from project_constants import PROCESSOR_STOP, PROCESSOR_PAUSE

class ProcessorInterface(ABC):

    def __init__(self, name:str, bufSize=3):
        self.__name = name
        self.__data = []
        self.__result = []
        self.__bufSize= bufSize
        self.__lock = Lock()

    @abstractmethod
    def __prepare__(self) -> None: pass
    
    @abstractmethod
    def processing(self, section: Section): pass

    def pop(self, data_list):
        with self.__lock:
            if data_list:
                return data_list.pop(0)

    def append(self, data_list, item):
        with self.__lock:
            data_list.append(item)

    def run(self, flag):
        data = self.__data
        result = self.__result
        loger = Loger(self.__name+"-thread")
        loger("start") # loger
        timer = Timer() # timer
        while True:
            if flag.value == PROCESSOR_PAUSE:
                time.sleep(0.1)
            elif flag.value == PROCESSOR_STOP:
                break
            else:
                if len(data) > 0:
                    dt = self.pop(data)
                    timer.start() # timer
                    self.append(result, self.processing(dt))
                    timer.end() # timer
                    loger(dt.index, "데이터 연산 완료", option=timer) # loger

    def __call__(self, data: Queue, result: Queue, flag: Value, transceiver:TransceiverInterface): # type: ignore
        loger = Loger(self.__name) # logger
        buffer = self.__data
        bufSize = self.__bufSize
        resultBuffer = self.__result
        try:
            self.__prepare__()

            th = Thread(target=self.run, args=(flag,))
            th.start()

            timer = Timer() # timer
            loger("start") # loger
            while True:
                if flag.value == PROCESSOR_PAUSE:
                    time.sleep(0.1)
                elif flag.value == PROCESSOR_STOP:
                    break
                else:
                    if not data.empty() and len(buffer) < bufSize:
                        timer.start() # timer
                        ret, data_ = transceiver.receive(data)
                        timer.end() # timer
                        loger("데이터 수신 후 압축 해제", option=timer) # loger
                        if ret:
                            self.append(buffer, data_)
                    if len(resultBuffer) > 0:
                        timer.start() # timer
                        transceiver.send(result, self.pop(resultBuffer))
                        timer.end() # timer
                        loger("데이터 압축 후 전송", option=timer) # loger

            loger(os.getpid(), "연산 프로세서 종료", option="terminate")
        except Exception as e:
            flag.value = PROCESSOR_STOP
            loger(os.getpid(), "연산 프로세서 오류", e)
        th.join(1)
        return