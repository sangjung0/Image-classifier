from multiprocessing.sharedctypes import SynchronizedBase 
from threading import Thread
import os
import time

from image_data.buffer import Sender
from image_data.model import Section
from image_data.logic import StartPointInterface
from image_data.transceiver import Interface as TI

from project_constants import PROCESSOR_STOP, PROCESSOR_PAUSE

from util.util import Timer, Loger

class StartPoint:
    def __init__(self, name: str, bufSize:int, logic:StartPointInterface) -> None:
        self.__name = name
        self.__isFinish = False
        self.__bufSize = bufSize
        self.__logic = logic
            
    def setIsFinish(self, value: bool) -> None:
        if isinstance(value, bool):
            self.__isFinish = value
        else:
            raise ValueError("isFinish is must be boolean")

    def __call__(self, order:int, terminationSignal:SynchronizedBase, flag: SynchronizedBase, lastIndex:SynchronizedBase, transceiver:TI) -> None: 
        loger = Loger(self.__name) # logger
        timer = Timer() # timer
        loger("start") # loger
        self.__logic.prepare(self.setIsFinish)
        index = 0
        bufSize = self.__bufSize
        try:
            sender = Sender(self.__name+"-Sender", logerIsPrint=True)
            th = Thread(target=sender, args=(order+1, terminationSignal, flag, transceiver))
            th.start()

            while True:
                if flag.value == PROCESSOR_PAUSE:
                    time.sleep(0.1)
                elif flag.value == PROCESSOR_STOP:
                    break
                else:
                    if index - lastIndex.value < bufSize:
                        data = timer.measure(lambda :self.__logic.processing(Section(index, [])))
                        loger("데이터 연산", option=timer)
                        index += 1

                        sender.append(data)
                        if self.__isFinish:
                            terminationSignal.value += 1
                            break
                    else:
                        time.sleep(0.01)
        except Exception as e:
            flag.value = PROCESSOR_STOP
            loger(os.getpid(), "오류", e)
        loger(f"연산 평균 속도 {timer.average}", option='result')
        th.join()
        loger(os.getpid(), "종료", option="terminate")
        return