from multiprocessing.sharedctypes import SynchronizedBase

from program.core.scheduler.transceiver import Receiver
from program.core.scheduler.dto import Packet


class Processor:
    def __init__(self, buf_size: int):
        self.__buf_size: int

    def __call__(self, order: int, termination_signal: SynchronizedBase, flag: SynchronizedBase,
                 receiver: Receiver): pass

    def processing(self, packet: Packet): pass
