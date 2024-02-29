from abc import abstractmethod
from multiprocessing import Queue, Value
from threading import Thread
import os
import time

from video.buffer import Sender, Receiver
from video.logic import StopOverPointInterface
from util import TransceiverInterface
from util.util import Timer, Loger
from project_constants import PROCESSOR_STOP, PROCESSOR_PAUSE

class StopOverPoint:
    def __init__(self, name: str, bufSize:int, logic:StopOverPointInterface):
        self.__name = name
        self.__bufSize = bufSize
        self.__logic = logic

    def __call__(self, order:int, terminationSignal:Value, flag: Value, inputQ: Queue, outputQ: Queue, transceiver:TransceiverInterface): # type: ignore
        loger = Loger(self.__name) # logger
        timer = Timer() # timer
        loger("start") # loge
        self.__logic.prepare()
        try:
            receiver = Receiver(self.__name+"-Receiver", self.__bufSize, logerIsPrint=True)
            receiverTh = Thread(target=receiver, args=(order, terminationSignal, flag, inputQ, transceiver))
            receiverTh.start()

            sender = Sender(self.__name+"-Sender", logerIsPrint=True)
            senderTh = Thread(target=sender, args=(order+1, terminationSignal, flag, outputQ, transceiver))
            senderTh.start()

            while True:
                if flag.value == PROCESSOR_PAUSE:
                    time.sleep(0.1)
                elif flag.value == PROCESSOR_STOP:
                    break
                else:
                    if receiver.empty():
                        if terminationSignal.value == order:
                            terminationSignal.value += 1
                            break
                        time.sleep(0.01)
                    else:
                        data = receiver.get()
                        result = timer.measure(lambda : self.__logic.processing(data))
                        loger("데이터 연산", option=timer)
                        sender.append(result)
            loger(os.getpid(), "종료", option="terminate")
        except Exception as e:
           flag.value = PROCESSOR_STOP
           loger(os.getpid(), "오류", e)
        loger(f"연산 평균 속도 {timer.average}", option='result')
        receiverTh.join()
        senderTh.join()
        return