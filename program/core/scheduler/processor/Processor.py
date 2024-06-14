from multiprocessing.sharedctypes import SynchronizedBase
from multiprocessing import Queue
from threading import Thread
import os
import time
import gc

from core.scheduler.transceiver import Receiver, Sender
from core.scheduler.dto import Packet
from core.Constant import PROCESSOR_STOP, PROCESSOR_PAUSE

from utils import Loger, Timer

class Processor:
    """멀티 프로세싱의 기반이 되는 클래스"""
    def __init__(self, name:str, loger_is_print:bool = False)->None:
        self.__name:str = name
        self.__loger_is_print:bool = loger_is_print

    def __call__(self, order: int, termination_signal: SynchronizedBase, flag: SynchronizedBase, input_q:Queue, output_q:Queue) -> None:
        # --
        loger = Loger(self.__name, self.__loger_is_print) # logger
        timer = Timer() # timer
        loger("start") # loge
        # --
        
        sender = None
        sender_thread = None
        receiver = None
        receiver_thread = None
        
        try:
            sender = Sender(self.__name + "Sender", self.__loger_is_print)
            sender_thread = Thread(target=sender, args=(order+1, termination_signal, flag, output_q))
            sender_thread.start()
            
            receiver = Receiver(self.__name + "Receiver", self.__loger_is_print)
            receiver_thread = Thread(target=receiver, args=(order, termination_signal, flag, input_q))
            receiver_thread.start()
            
            while True:
                if flag.value == PROCESSOR_STOP:
                    break
                elif flag.value == PROCESSOR_PAUSE or sender.is_full():
                    time.sleep(0.1)
                else:
                    if receiver.is_empty():
                        if not receiver_thread.is_alive():
                            break
                        time.sleep(0.01)
                    else:
                        data = receiver.get()
                        result = timer.measure(lambda : self.processing(data))
                        loger("데이터 연산", option=timer)
                        sender.append(result)
                    gc.collect()
        except Exception as e:
            flag.value = PROCESSOR_STOP
            loger(os.getpid(), "오류", e)
        if receiver_thread is not None: receiver_thread.join()
        if sender_thread is not None: sender_thread.join()
        loger(os.getpid(), "종료", option="terminate")
        termination_signal.value += 1
        
    def processing(self, value:Packet) -> Packet:
        raise Exception("구현 안됨")
            
