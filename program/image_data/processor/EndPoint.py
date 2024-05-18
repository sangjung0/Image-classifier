from multiprocessing.sharedctypes import SynchronizedBase
from threading import Thread
import os

from image_data.buffer import Receiver
from image_data.transceiver import Interface as TI

from project_constants import PROCESSOR_STOP

from util.util import Loger
        
class EndPoint:
    def __init__(self, name: str, bufSize:int) -> None:
        self.__name = name
        self.__bufSize = bufSize

    def __call__(self, order:int, terminationSignal:SynchronizedBase, flag: SynchronizedBase, transceiver:TI, requiresSorting:bool) -> tuple[Receiver, Thread]:
        loger = Loger(self.__name) # logger
        loger("start") # loger
        try:

            receiver = Receiver(self.__name+"-Receiver", self.__bufSize, logerIsPrint=True, requiresSorting=requiresSorting)
            receiverTh = Thread(target=receiver, args=(order, terminationSignal, flag, transceiver))
            receiverTh.start()

            return receiver, receiverTh
        
        except Exception as e:
            flag.value = PROCESSOR_STOP
            loger(os.getpid(), "오류", e)
        receiverTh.join()
        return
    

