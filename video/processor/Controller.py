from multiprocessing import Process, Queue, Value
from typing import Type
from video.model import Section

from video.processor.EndPoint import EndPoint
from video.processor.SinglePoint import SinglePoint
from video.processor.StartPoint import StartPoint
from video.processor.StopOverPoint import StopOverPoint
from video.logic import StopOverPointInterface, StartPointInterface
from util import CompressorInterface, TransceiverInterface
from util.util import AllProcessIsTerminated, AllTransmissionMediumIsTerminated
from project_constants import PROCESSOR_PAUSE


class Controller:

    #logics First element is must be StartPointInterface
    @staticmethod
    def getSingle(logics:list[object], name:str, compressor:Type[CompressorInterface]):
        """ 
        Logics First element is must be StartPointInterface, Another elements is must be StopOverPointInterface
        """
        return SinglePoint(name,StartPointLogics(logics), compressor=compressor())

    @staticmethod
    def get(logics:list[list[object]], 
            pNumbers:list[int], 
            compressor: Type[CompressorInterface],
            transceiver: Type[TransceiverInterface],
            pBufSize:list[int],
            names:list[str]
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
        for logic, pb, n, pn in zip(logics, pBufSize, names, pNumbers):
            queues.append(Queue())
            stopOverPoint = StopOverPoint(n, pb, StopOverPointLogics(logic))
            for _ in range(pn):
                terminationOrder += 1
                stopOverProcess.append(
                    Process(
                        target=stopOverPoint,
                        args=(terminationOrder, terminationSignal, flag, queues[-2],queues[-1], transceiver)
                    )
                )
        
        endPoint = EndPoint(endPointName, endPointPBufSize)

        startProcess.start()
        for p in stopOverProcess: p.start()
        receiver, receiverTh = endPoint(terminationOrder + 1, terminationSignal, flag, lastIndex, queues[-1], transceiver)

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
