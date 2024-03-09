from multiprocessing import Process, Queue, Value
from multiprocessing.sharedctypes import SynchronizedBase
from threading import Thread
from typing import Type

from process.processor.EndPoint import EndPoint
from process.processor.SinglePoint import SinglePoint
from process.processor.StartPoint import StartPoint
from process.processor.StopOverPoint import StopOverPoint

from process.buffer import Receiver
from process.model import Section
from process.logic import StopOverPointInterface, StartPointInterface
from process.compressor import CompressorInterface
from process.transceiver import TransceiverInterface

from project_constants import PROCESSOR_PAUSE


class StartPointLogics(StartPointInterface):
    def __init__(self, logics:list[StartPointInterface]) -> None:
        self.__logics = logics

    def prepare(self, setIsFinish: callable) -> None:
        logics = self.__logics
        for logic in logics:
            if logic is logics[0]:
                logic.prepare(setIsFinish)
            else:
                logic.prepare()

    def processing(self, section:Section) -> Section:
        for logic in self.__logics:
            section = logic.processing(section)
        return section      
    
class StopOverPointLogics(StopOverPointInterface):
    def __init__(self, logics:list[StopOverPointInterface]) -> None:
        self.__logics = logics

    def prepare(self) -> None:
        for logic in self.__logics:
            logic.prepare()

    def processing(self, section:Section) -> Section:
        for logic in self.__logics:
            section = logic.processing(section)
        return section

class AllProcessIsTerminated:
    def __init__(self, processes:list[Process]) -> None:
        self.__processes = processes

    def allProcessIsTerminated(self) -> bool:
        return not any(p.is_alive() for p in self.__processes)
    
    def wait(self) -> None:
        for p in self.__processes:
            p.join(1)
            if p.is_alive(): p.terminate()

class AllTransmissionMediumIsTerminated:
    def __init__(self, mediums:list[Queue]) -> None:
        self.__mediums = mediums
    
    def wait(self) -> None:
        for m in self.__mediums:
            m.close()
            m.join_thread()

class Controller:

    #logics First element is must be StartPointInterface
    @staticmethod
    def getSingle(name:str, logics:list[object]) -> SinglePoint:
        """ 
        Logics First element is must be StartPointInterface, Another elements is must be StopOverPointInterface
        """
        return SinglePoint(name,StartPointLogics(logics))

    @staticmethod
    def get(
            names:list[str],
            logics:list[list[object]], 
            pNumbers:list[int],
            pBufSize:list[int],
            bufSort:list[bool],
            compressor: Type[CompressorInterface],
            transceiver: Type[TransceiverInterface]
        ) -> tuple[SynchronizedBase, Receiver, Thread, AllProcessIsTerminated, AllTransmissionMediumIsTerminated]:
        """ 
        Logics First element is must be StartPointInterface, Another elements is must be StopOverPointInterface
        """
        startPointLogics = logics.pop(0)
        startPointName = names.pop(0)
        startPointPBufSize = pBufSize.pop(0)
        endPointName = names.pop()
        endPointPBufSize = pBufSize.pop()

        flag:SynchronizedBase = Value('i',PROCESSOR_PAUSE)
        lastIndex:SynchronizedBase = Value('i', 0)
        terminationSignal:SynchronizedBase = Value('i', 0)
        terminationOrder = 0

        queues:list[Queue] = [Queue()]

        startProcess = Process(
            target=StartPoint(startPointName,startPointPBufSize,StartPointLogics(startPointLogics)),
            args=(terminationSignal, flag, lastIndex, queues[0], transceiver, compressor)
        )
        
        stopOverProcess:list[Process] = []
        for logic, pb, bs, n, pn in zip(logics, pBufSize, bufSort, names, pNumbers):
            queues.append(Queue())
            stopOverPoint = StopOverPoint(n, pb, StopOverPointLogics(logic))
            for _ in range(pn):
                terminationOrder += 1
                stopOverProcess.append(
                    Process(
                        target=stopOverPoint,
                        args=(terminationOrder, terminationSignal, flag, queues[-2],queues[-1], transceiver, bs)
                    )
                )
        
        endPoint = EndPoint(endPointName, endPointPBufSize)

        startProcess.start()
        for p in stopOverProcess: p.start()
        receiver, receiverTh = endPoint(terminationOrder + 1, terminationSignal, flag, lastIndex, queues[-1], transceiver, True)

        allProcess = AllProcessIsTerminated([startProcess] + stopOverProcess)
        allTransmissionMedium = AllTransmissionMediumIsTerminated(queues)

        return flag, receiver, receiverTh, allProcess, allTransmissionMedium