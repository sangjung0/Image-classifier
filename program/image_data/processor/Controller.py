from multiprocessing import Process, Queue, Value, Array
from multiprocessing.sharedctypes import SynchronizedBase
from threading import Thread
from typing import Type
from functools import reduce
import numpy as np

from image_data.processor.EndPoint import EndPoint
from image_data.processor.SinglePoint import SinglePoint
from image_data.processor.StartPoint import StartPoint
from image_data.processor.StopOverPoint import StopOverPoint
from image_data.processor.SharedStartPoint import SharedStartPoint
from image_data.processor.ConnectPoint import ConnectPoint

from image_data.buffer import Receiver
from image_data.model import Section
from image_data.logic import StopOverPointInterface, StartPointInterface
from image_data.serializer import Interface as SI 
from image_data.compressor import Interface as CI
from image_data.transceiver import SharedMemory as ST
from image_data.transceiver import Queue as QT

from project_constants import PROCESSOR_PAUSE, CHARACTER_SIZE, PHASE_SIZE, ORDER_SIZE, SCALE_SIZE


class StartPointLogics(StartPointInterface):
    """
    
    """
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
    """
    
    """
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
            sharedPNames:list[str],                 # 프로세서 이름
            sharedLogics:list[list[object]],        # 공유메모리를 사용하는 로직 순서
            sharedPNumbers:list[int],               # 공유메모리를 사용할 프로세서 개수
            sharedBufSize:list[int],                # 공유메모리를 사용할 프로세서의 버프 크기
            sharedBufSort:list[bool],               # 공유메모리를 사용할 프로세서의 버프 정렬 유무
            sharedTransceiver: Type[ST],            # 공유메모리에 사용할 데이터 교환기
            sharedMemorySize: int,                  # 공유 메모리의 크기
            batchSize:int,                          # 배치 사이즈
            dataSize: tuple,                        # 공유 메모리에 담을 데이터 크기
            queuePNames:list[str],                  # 프로세서 이름
            queueLogics:list[list[object]],         # 큐를 사용하는 로직 순서
            queuePNumbers:list[int],                # 큐를 사용할 프로세서 개수
            queueBufSize:list[int],                 # 큐를 사용할 프로세서의 버프 크기
            queueBufSort:list[bool],                # 큐를 사용할 프로세서의 버프 정렬 유무
            queueTransceiver: Type[QT],             # 큐에 사용할 데이터 교환기
            compressor: CI,                         # 큐에서 전송할 데이터 압축 로직
            serializer: SI,                         # 큐에서 전송할 데이터 직렬화 로직
            queueSize: int,                         # 큐 사이즈
        ) -> tuple[SynchronizedBase, Receiver, Thread, AllProcessIsTerminated, AllTransmissionMediumIsTerminated]:
        """
        Logics First element is must be StartPointInterface, Another elements is must be StopOverPointInterface
        """

        flag:SynchronizedBase = Value('i',PROCESSOR_PAUSE)
        terminationSignal:SynchronizedBase = Value('i', -1)
        memorySize = (sharedMemorySize, PHASE_SIZE + ORDER_SIZE + SCALE_SIZE + CHARACTER_SIZE + reduce(lambda x,y: x*y, dataSize))
        sharedMemory = Array('b', memorySize[0] * memorySize[1])
        makeQueue = lambda:Queue(maxsize=queueSize)
        queues:list[Queue] = [makeQueue()]

        phaseOrder = 0
        terminationOrder = 0

        startPointName = sharedPNames.pop(0)
        startPointLogics = sharedLogics.pop(0)
        startPointPNumbers = sharedPNumbers.pop(0) # 사용되지 않음
        startPointBufSize = sharedBufSize.pop(0) 
        startPointBufSort = sharedBufSort.pop(0) # 사용되지 않음
        
        connectPointName = sharedPNames.pop()
        connectPointLogics = sharedLogics.pop()
        connectPointPNumbers = sharedPNumbers.pop()
        connectPointBufSize = sharedBufSize.pop()
        connectPointBufSort = sharedBufSort.pop()
        
        # 공유메모리 프로세스
        sharedStopOverProcess:list[Process] = []
        for n, lo, pn, sz, st,  in zip(sharedPNames, sharedLogics, sharedPNumbers, sharedBufSize, sharedBufSort):
            stopOverPoint = StopOverPoint(n, sz, StopOverPointLogics(lo))
            phaseOrder += 1
            prevPhase = phaseOrder
            nextPhase = prevPhase + pn + 1
            terminationOrder += 1
            for _ in range(pn):
                phaseOrder += 1
                transceiver = sharedTransceiver(sharedMemory, memorySize, dataSize, batchSize, prevPhase, phaseOrder, nextPhase)
                sharedStopOverProcess.append(
                    Process(
                        target=stopOverPoint,
                        args=(terminationOrder, terminationSignal, flag, transceiver, transceiver, st)
                    )
                )
        
        # 공유메모리 마지막 프로세스, 큐 프로세스와 연결
        connectProcess = ConnectPoint(connectPointName, connectPointBufSize, StopOverPointLogics(connectPointLogics))
        phaseOrder += 1
        prevPhase = phaseOrder
        nextPhase = phaseOrder + connectPointPNumbers + 1
        terminationOrder += 1
        for _ in range(connectPointPNumbers):
            phaseOrder += 1
            receiver = sharedTransceiver(sharedMemory, memorySize, dataSize, batchSize, prevPhase, phaseOrder, nextPhase)
            sender = queueTransceiver(queues[0], serializer, compressor)
            sharedStopOverProcess.append(
                Process(
                    target=connectProcess,
                    args=(terminationOrder, terminationSignal, flag, sender, receiver, connectPointBufSort)
                )
            )
            
        # 공유메모리 첫번째 프로세스
        phaseOrder += 1
        np.ndarray(memorySize, dtype=np.byte, buffer=sharedMemory.get_obj())[:] = phaseOrder
        transceiver = sharedTransceiver(sharedMemory, memorySize, dataSize, batchSize, phaseOrder, 0, 1)
        startProcess = Process(
            target=SharedStartPoint(startPointName, startPointBufSize, StartPointLogics(startPointLogics)),
            args=(0, terminationSignal, flag, transceiver, transceiver)
        )

        endPointName = queuePNames.pop()
        endPointLogics = queueLogics.pop() # 사용되지 않음 
        endPointPNumbers = queuePNumbers.pop() # 사용되지 않음
        endPointBufSize = queueBufSize.pop()
        endPointBufSort = queueBufSort.pop()

        # 큐 프로세스
        queueStopOverProcess:list[Process] = []
        for n, lo, pn, sz, st,  in zip(queuePNames, queueLogics, queuePNumbers, queueBufSize, queueBufSort):
            queues.append(makeQueue())
            stopOverPoint = StopOverPoint(n, sz, StopOverPointLogics(lo))
            receiver = queueTransceiver(queues[-2], serializer, compressor)
            sender = queueTransceiver(queues[-1], serializer, compressor)
            terminationOrder += 1
            for _ in range(pn):
                queueStopOverProcess.append(
                    Process(
                        target=stopOverPoint,
                        args=(terminationOrder, terminationSignal, flag, sender, receiver, st)
                    )
                )

        # 마지막 프로세스
        endPoint = EndPoint(endPointName, endPointBufSize)
        receiver, receiverTh = endPoint(terminationOrder+1, terminationSignal, flag, queueTransceiver(queues[-1], serializer, compressor), endPointBufSort)

        startProcess.start()
        for p in sharedStopOverProcess: p.start()
        for p in queueStopOverProcess: p.start()

        allProcess = AllProcessIsTerminated([startProcess] + sharedStopOverProcess + queueStopOverProcess)
        allTransmissionMedium = AllTransmissionMediumIsTerminated(queues)

        return flag, receiver, receiverTh, allProcess, allTransmissionMedium