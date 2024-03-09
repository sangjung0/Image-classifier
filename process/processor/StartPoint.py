from multiprocessing import Queue, Value
from threading import Thread, Lock
from typing import Type
import os
import time

from process.buffer import Sender
from process.model import Section
from process.logic import StartPointInterface
from process.compressor import CompressorInterface
from process.transceiver import TransceiverInterface

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

    def __call__(self, terminationSignal:Value, flag: Value, lastIndex:Value, outputQ: Queue, transceiver:TransceiverInterface, compressor: Type[CompressorInterface]) -> None: # type: ignore
        loger = Loger(self.__name) # logger
        timer = Timer() # timer
        loger("start") # loger
        self.__logic.prepare(self.setIsFinish)
        index = 0
        bufSize = self.__bufSize
        compressor = compressor()
        try:
            sender = Sender(self.__name+"-Sender", logerIsPrint=True)
            th = Thread(target=sender, args=(1, terminationSignal, flag, outputQ, transceiver))
            th.start()

            while True:
                if flag.value == PROCESSOR_PAUSE:
                    time.sleep(0.1)
                elif flag.value == PROCESSOR_STOP:
                    break
                else:
                    if index - lastIndex.value < bufSize:
                        data = timer.measure(lambda :self.__logic.processing(Section(index, [], compressor=compressor)))
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