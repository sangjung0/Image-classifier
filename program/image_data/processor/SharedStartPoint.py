from multiprocessing.sharedctypes import SynchronizedBase
from threading import Thread
import os
import time

from image_data.buffer import Sender, Receiver
from image_data.logic import StartPointInterface
from image_data.transceiver import Interface as TI

from project_constants import PROCESSOR_STOP, PROCESSOR_PAUSE

from util.util import Timer, Loger

class SharedStartPoint:
    def __init__(self, name: str, bufSize:int, logic:StartPointInterface, isPrint:bool = True) -> None:
        self.__name = name
        self.__isFinish = False
        self.__bufSize = bufSize
        self.__logic = logic
        self.__isPrint = isPrint
            
    def setIsFinish(self, value: bool) -> None:
        if isinstance(value, bool):
            self.__isFinish = value
        else:
            raise ValueError("isFinish is must be boolean")

    def __call__(self, order:int, terminationSignal:SynchronizedBase, flag:SynchronizedBase, recceiverTransceiver:TI, senderTransceiver:TI) -> None:
        loger = Loger(self.__name, self.__isPrint) # logger
        timer = Timer() # timer
        loger("start") # loger
        self.__logic.prepare(self.setIsFinish)
        try:
            receiver = Receiver(self.__name+"-Receiver", self.__bufSize, logerIsPrint=True)
            receiverTh = Thread(target=receiver, args=(order, terminationSignal, flag, recceiverTransceiver))
            receiverTh.start()

            sender = Sender(self.__name+"-Sender", logerIsPrint=True)
            senderTh = Thread(target=sender, args=(order+1, terminationSignal, flag, senderTransceiver))
            senderTh.start()

            while True:
                if flag.value == PROCESSOR_PAUSE:
                    time.sleep(0.1)
                elif flag.value == PROCESSOR_STOP:
                    break
                else:
                    if self.__isFinish:
                        terminationSignal.value += 1
                        break
                    elif receiver.empty():
                        time.sleep(0.01)
                    else:
                        data = receiver.get()
                        result = timer.measure(lambda :self.__logic.processing(data))
                        loger("데이터 연산", option=timer)
                        sender.append(result)
        except Exception as e:
            flag.value = PROCESSOR_STOP
            loger(os.getpid(), "오류", e)
        loger(f"연산 평균 속도 {timer.average}", option='result')
        receiverTh.join()
        senderTh.join()
        loger(os.getpid(), "종료", option="terminate")
        return