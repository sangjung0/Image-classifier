from typing import Type

from image_data.logic import *
from image_data.processor import Controller as PC
from image_data.Loader import Loader, SingleLoader
from image_data.compressor import Interface as CI
from image_data.compressor import UnCompressor
from image_data.serializer import Interface as SI
from image_data.serializer import Pickle
from image_data.transceiver import Interface as TI
from image_data.transceiver import Queue as QT
from image_data.transceiver import SharedMemory
from image_data.PathData import PathData
from image_data.face_detector import DetectorInterface


class Controller:

    @staticmethod
    def startSingleAndGetVideoLoader(
        path:str, detector:Type[DetectorInterface], imageSize:tuple=(480, 640, 3)
    ) -> SingleLoader:
        pathData = PathData(path)

        logics = [Distributor(pathData, imageSize), Detector(detector), ExtractMetaData()]

        process = PC.getSingle("singleProcessor", logics)

        return SingleLoader(pathData, process)

    @staticmethod
    def startAndGetVideoLoader(
        path:str, detector:Type[DetectorInterface], sharedMemorySize:int = 128, batchSize:int= 64, imageSize:tuple=(480, 640, 3), queueSize:int=256, bufSize:int=64,
        queueTransceiver:Type[TI] = QT, sharedTransceiver:Type[TI] = SharedMemory, 
        compressor:CI = UnCompressor(), serializer:SI = Pickle(),
        detectProcessorNumber:int=1
        ) -> Loader:

        pathData = PathData(path)

        sharedPNames = []
        sharedLogics = []
        sharedPNumbers = []
        sharedBufSize = []
        sharedBufSort = []
        queuePNames = []
        queueLogics = []
        queuePNumbers = []
        queueBufSize = []
        queueBufSort = []

        # Distributor 세팅
        sharedPNames.append("StartProcess")
        sharedLogics.append([Distributor(list(pathData), imageSize)])
        sharedPNumbers.append(1)
        sharedBufSize.append(bufSize)
        sharedBufSort.append(False)

        # detector 세팅
        sharedPNames.append("DetectProcess")
        sharedLogics.append([Detector(detector)])
        sharedPNumbers.append(detectProcessorNumber)
        sharedBufSize.append(bufSize)
        sharedBufSort.append(False)

        
        # extractMetaData 세팅
        queuePNames.append("MetadataProcess")
        queueLogics.append([ExtractMetaData()])
        queuePNumbers.append(1)
        queueBufSize.append(bufSize)
        queueBufSort.append(False)

        # endPoint 세팅
        queuePNames.append("EndPoint")
        queueLogics.append([])
        queuePNumbers.append(1)
        queueBufSize.append(bufSize)
        queueBufSort.append(False)

        flag, receiver, receiverTh, allProcess, allTransmissionMedium = PC.get(
            sharedPNames, sharedLogics, sharedPNumbers, sharedBufSize, sharedBufSort, sharedTransceiver, sharedMemorySize, batchSize, imageSize,
            queuePNames, queueLogics, queuePNumbers, queueBufSize, queueBufSort, queueTransceiver,compressor, serializer, queueSize)

        return Loader(pathData, receiver, receiverTh, flag, allProcess, allTransmissionMedium)