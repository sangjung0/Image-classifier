from typing import Type

from process.face_detector import DetectorInterface
from process.tracker import TrackerInterface
from process.VideoData import VideoData
from process.logic import *
from process.processor import Controller as PC
from process.Loader import Loader, SingleLoader
from process.compressor import CompressorInterface, UnCompressor
from process.serializer import PickleSerializer
from process.transceiver import TransceiverInterface, Transceiver
from process.scene_detector import Interface
from process.model import Face

class Controller:

    @staticmethod
    def playSingleFromFaces(fileName:str, faces:list[Face], cfl:int= 200, draw:bool = False):
        videoData = VideoData(fileName)
        logics = [
            Distributor(videoData, 1, cfl),
            InsertFace(faces)
        ]

        if draw:
            logics.append(FaceVisualizer())

        process = PC.getSingle("singleProcessor", logics)

        return SingleLoader(videoData, process)

    @staticmethod
    def startSingleAndGetVideoLoader(
        fileName:str, detectFrameCount:int = 1, scale:int = 1, cfl:int = 200, pointNumber:int = 1000,
        filter = None, detector:Type[DetectorInterface] = None, tracker:Type[TrackerInterface] = None, sceneDetector:Type[Interface] = None, draw:bool = False
    ):
        videoData = VideoData(fileName)
        colors = set()

        if detector is not None: colors.add(detector.COLOR)
        if tracker is not None: colors.add(tracker.COLOR)

        logics = [
            Distributor(videoData, detectFrameCount, cfl), 
            Vision(filter, videoData.width, videoData.height, scale, colors, draw)
        ]

        if sceneDetector is not None:
            logics.append(SceneDetector(sceneDetector))

        if detector is not None:
            logics.append(Detector(detector, scale))

        if tracker is not None:
            logics.append(Tracker(tracker, scale))
            logics.append(FaceTracker())

        if draw:
            logics.append(FaceVisualizer())
            logics.append(TraceLineVisualizer(pointNumber))


        process = PC.getSingle("singleProcessor", logics)

        return SingleLoader(videoData, process)


    @staticmethod
    def startAndGetVideoLoader(
        fileName:str, visionProcessorNumber:int = 1, detectProcessorNumber:int=1,  trackerProcessorNumber:int=1, detectFrameCount:int = 1, scale:int = 1, cfl:int = 200, bufSize:int = 64, pointNumber:int = 1000,
        transceiver:TransceiverInterface = Transceiver(PickleSerializer(), UnCompressor()), compressor: Type[CompressorInterface] = UnCompressor(),
        filter = None, detector:Type[DetectorInterface] = None, tracker:Type[TrackerInterface] = None, sceneDetector:Type[object] = None, draw:bool = False
        ):

        videoData = VideoData(fileName)
        colors = set()

        if detector is not None: colors.add(detector.COLOR)
        if tracker is not None: colors.add(tracker.COLOR)
        
        logics = [
            [
                Distributor(videoData, detectFrameCount, cfl), 
                Vision(filter, videoData.width, videoData.height, scale, colors, draw),
                Tracker(tracker,scale)
            ]
        ]
        pNumbers = []
        pBufSize = [bufSize]
        bufSort = []
        names = ["StartProcess"]

        if sceneDetector is not None:
            logics[0].append(SceneDetector(sceneDetector))

        if detector is not None:
            logics.append([
                Detector(detector, scale)
            ])
            names.append("DetectProcess")
            pNumbers.append(detectProcessorNumber)
            pBufSize.append(3)
            bufSort.append(True)

        # if tracker is not None:
        #     logics.append([
        #         Tracker(tracker, scale),
        #         FaceTracker()
        #     ])
        #     names.append("TrackerProcess")
        #     pNumbers.append(trackerProcessorNumber)
        #     pBufSize.append(3)

        if draw:
            logics.append([
                FaceTracker(),
                FaceFilter(videoData.width, videoData.height, 0),
                FaceVisualizer(),
                TraceLineVisualizer(pointNumber)
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

        return Loader(videoData, receiver, receiverTh, flag, allProcess, allTransmissionMedium)