from multiprocessing import Queue, Value
from threading import Thread
import os

from video.buffer import Receiver
from video.transceiver import TransceiverInterface

from project_constants import PROCESSOR_STOP

from util.util import Loger

class EndPoint:
    def __init__(self, name: str, bufSize:int):
        self.__name = name
        self.__bufSize = bufSize

    def __call__(self, order:int, terminationSignal:Value, flag: Value, lastIndex:Value, inputQ: Queue, transceiver:TransceiverInterface, requiresSorting:bool): # type: ignore
        loger = Loger(self.__name) # logger
        loger("start") # loger
        try:

            receiver = EndReceiver(self.__name+"-Receiver", self.__bufSize, lastIndex, logerIsPrint=True, requiresSorting = requiresSorting)
            receiverTh = Thread(target=receiver, args=(order, terminationSignal, flag, inputQ, transceiver))
            receiverTh.start()

            return receiver, receiverTh
        
        except Exception as e:
            flag.value = PROCESSOR_STOP
            loger(os.getpid(), "오류", e)
        receiverTh.join()
        return
    
class EndReceiver(Receiver):
    def __init__(self, name:str, bufSize: int, lastIndex:Value, requiresSorting: bool = False, logerIsPrint: bool = False) -> None: # type: ignore
        super().__init__(name, bufSize, requiresSorting, logerIsPrint)
        self.__lastIndex = lastIndex

    def append(self, value: object) -> None:
        super().append(value)
        self.__lastIndex.value = value.index
