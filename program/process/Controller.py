from typing import Type

from process.logic import *
from process.processor import Controller as PC
from process.Loader import Loader, SingleLoader
from process.compressor import CompressorInterface, UnCompressor
from process.serializer import PickleSerializer
from process.transceiver import TransceiverInterface, Transceiver
from process.PathData import PathData
from process.face_detector import DetectorInterface


class Controller:

    @staticmethod
    def startSingleAndGetVideoLoader(
        path:str, scale:int = 1, cfl:int = 200,
        filter = None, detector:Type[DetectorInterface] = None, draw:bool = False
    ) -> SingleLoader:
        pathData = PathData(path)
        colors = set()

        if detector is not None: colors.add(detector.COLOR)

        logics = [
            Distributor(pathData, cfl), 
            Vision(filter, scale, colors, draw)
        ]

        if detector is not None:
            logics.append(Detector(detector, scale))
            logics.append(FaceResizer(0))

        if draw:
            logics.append(FaceVisualizer())


        process = PC.getSingle("singleProcessor", logics)

        return SingleLoader(pathData, process)

    @staticmethod
    def startAndGetVideoLoader(
        path:str, visionProcessorNumber:int = 1, detectProcessorNumber:int=1, scale:int = 1, cfl:int = 200, bufSize:int = 64,
        transceiver:TransceiverInterface = Transceiver(PickleSerializer(), UnCompressor()), compressor: Type[CompressorInterface] = UnCompressor(),
        filter = None, detector:Type[DetectorInterface] = None, draw:bool = False
        ) -> Loader:

        pathData = PathData(path)
        colors = set()

        if detector is not None: colors.add(detector.COLOR)
        
        logics = [
            [
                Distributor(pathData, cfl), 
                Vision(filter, scale, colors, draw)
            ]
        ]
        pNumbers = []
        pBufSize = [bufSize]
        bufSort = []
        names = ["StartProcess"]

        if detector is not None:
            logics.append([
                Detector(detector, scale)
            ])
            names.append("DetectProcess")
            pNumbers.append(detectProcessorNumber)
            pBufSize.append(3)
            bufSort.append(True)

        if draw:
            logics.append([
                #FaceResizer(0),
                FaceVisualizer()
            ])
            names.append("Drawers")
            pNumbers.append(1)
            pBufSize.append(3)
            bufSort.append(True)

        if visionProcessorNumber != 1:
            raise Exception("이거 아직 안만듬 다시 만드셈")
        
        names.append("EndThread")
        pBufSize.append(3)

        flag, receiver, receiverTh, allProcess, allTransmissionMedium = PC.get(names, logics, pNumbers, pBufSize, bufSort, compressor, transceiver)

        return Loader(pathData, receiver, receiverTh, flag, allProcess, allTransmissionMedium)