from multiprocessing.sharedctypes import SynchronizedBase
from multiprocessing import Queue
from threading import Thread
import os
import time

from program.core.scheduler.transceiver import Receiver, Sender
from program.core.scheduler.dto import Packet
from core.scheduler.Constant import PROCESSOR_STOP, PROCESSOR_PAUSE

from utils import Loger, Timer

class Processor:
    def __init__(self, name:str, buf_size: int, loger_is_print:bool = False):
        self.__name:str = name
        self.__buf_size: int = buf_size
        self.__loger_is_print:bool = loger_is_print

    def __call__(self, order: int, termination_signal: SynchronizedBase, flag: SynchronizedBase, input_q:Queue, output_q:Queue):
        # --
        loger = Loger(self.__name) # logger
        timer = Timer() # timer
        loger("start") # loge
        # --
        try:
            sender = Sender(self.__name + "Receiver", self.__loger_is_print)
            sender_thread = Thread(target=sender, args=(order, termination_signal, flag, output_q))
            sender_thread.start()
            
            receiver = Receiver(self.__name + "Sender", self.__buf_size, self.__loger_is_print)
            receiver_thread = Thread(target=receiver, args=(order, termination_signal, flag, input_q))
            receiver_thread.start()
            
            while True:
                if flag.value == PROCESSOR_PAUSE:
                    time.sleep(0.1)
                elif flag.value == PROCESSOR_STOP:
                    break
                else:
                    if receiver.is_empty():
                        if termination_signal.value >= order:
                            termination_signal.value += 1
                            break
                        time.sleep(0.01)
                    else:
                        data = receiver.get()
                        result = timer.measure(lambda : self.processing(data))
                        loger("데이터 연산", option=timer)
                        sender.append(result)
            
        except Exception as e:
            flag.value = PROCESSOR_STOP
            loger(os.getpid(), "오류", e)
            
        
    def processing(self, value:Packet):
        raise Exception("구현 안됨")
            
