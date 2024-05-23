from multiprocessing.sharedctypes import SynchronizedBase

from program.core.scheduler.transceiver.Transceiver import Transceiver
from program.core.scheduler.dto import Converter


class Receiver(Transceiver):
    def __init__(self):
        super().__init__()
        self.__converter: Converter

    def __call__(self, order: int, termination_signal: SynchronizedBase, flag: SynchronizedBase):
        pass

    def is_full(self) -> bool:
        pass

