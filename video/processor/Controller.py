from multiprocessing import Process, Queue, Value
from typing import Type
from video.model import Section

from video.processor.EndPoint import EndPoint
from video.processor.SinglePoint import SinglePoint
from video.processor.StartPoint import StartPoint
from video.processor.StopOverPoint import StopOverPoint

from video.logic import StopOverPointInterface, StartPointInterface
from video.compressor import CompressorInterface
from video.transceiver import TransceiverInterface

from project_constants import PROCESSOR_PAUSE

class Controller:

    #logics First element is must be StartPointInterface
    @staticmethod
    def getSingle(name:str, logics:list[object]):
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
        ):
        """ 
        Logics First element is must be StartPointInterface, Another elements is must be StopOverPointInterface
        """
        startPointLogics = logics.pop(0)
        startPointName = names.pop(0)
        startPointPBufSize = pBufSize.pop(0)
        endPointName = names.pop()
        endPointPBufSize = pBufSize.pop()

        flag = Value('i',PROCESSOR_PAUSE)
        lastIndex = Value('i', 0)
        terminationSignal = Value('i', 0)
        terminationOrder = 0

        queues = [Queue()]

        startProcess= Process(
            target=StartPoint(startPointName,startPointPBufSize,StartPointLogics(startPointLogics)),
            args=(terminationSignal, flag, lastIndex, queues[0], transceiver, compressor)
        )
        
        stopOverProcess = []
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

        allProcess = AllProcessIsTerminated([startProcess, receiverTh] + stopOverProcess)
        allTransmissionMedium = AllTransmissionMediumIsTerminated(queues)

        return flag, receiver, allProcess, allTransmissionMedium

class StartPointLogics(StartPointInterface):
    def __init__(self, logics:list[object]):
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
    def __init__(self, logics:list[object]):
        self.__logics = logics

    def prepare(self) -> None:
        for logic in self.__logics:
            logic.prepare()

    def processing(self, section:Section) -> Section:
        for logic in self.__logics:
            section = logic.processing(section)
        return section

class AllProcessIsTerminated:
    def __init__(self, processes):
        self.__processes = processes

    def allProcessIsTerminated(self):
        return not any(p.is_alive() for p in self.__processes)
    
    def wait(self):
        for p in self.__processes:
            p.join(1)
            if p.is_alive(): p.terminate()

class AllTransmissionMediumIsTerminated:
    def __init__(self, mediums):
        self.__mediums = mediums
    
    def wait(self):
        for m in self.__mediums:
            m.close()
            m.join_thread()

