from multiprocessing import Queue, Value
from threading import Thread
from typing import Type
import os
import time

from video.buffer import Sender
from video.model import Section
from video.logic import StartPointInterface
from util import CompressorInterface, TransceiverInterface
from util.util import Timer, Loger
from project_constants import PROCESSOR_STOP, PROCESSOR_PAUSE

class StartPoint:
    def __init__(self, name: str, bufSize:int, logic:StartPointInterface):
        self.__name = name
        self.__isFinish = False
        self.__bufSize = bufSize
        self.__logic = logic

    def setIsFinish(self, value):
        if isinstance(value, bool):
            self.__isFinish = value
        else:
            raise ValueError("isFinish is must be boolean")

    def __call__(self, terminationSignal:Value, flag: Value, lastIndex:Value, outputQ: Queue, transceiver:TransceiverInterface, compressor: Type[CompressorInterface]): # type: ignore
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
                        data = timer.measure(lambda :self.__logic.processing())
                        loger("데이터 연산", option=timer)

                        index = data.index
                        videoSection = Section(index, [], compressor=compressor)
                        for i in data:
                            videoSection.append(i)
                        sender.append(videoSection)
                        if self.__isFinish:
                            terminationSignal.value += 1
                            break
                    else:
                        time.sleep(0.01)
        except Exception as e:
            flag.value = PROCESSOR_STOP
            loger(os.getpid(), "오류", e)
        loger(os.getpid(), "종료", option="terminate")
        loger(f"연산 평균 속도 {timer.average}", option='result')
        th.join()
        return