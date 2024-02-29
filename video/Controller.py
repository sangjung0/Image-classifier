from typing import Type

from face_detector import DetectorInterface
from face_tracker import TrackerInterface

from video.VideoData import VideoData
from video.logic import Distributor, Vision, Detector, SceneDetector, Tracker, DetectorVisualizer
from video.processor import Controller as PC
from video.Loader import Loader
from util import CompressorInterface, UnCompressor, PickleSerializer, TransceiverInterface, Transceiver

class Controller:
    @staticmethod
    def startAndGetVideoLoader(
        fileName:str, visionProcessorNumber:int = 1, detectProcessorNumber:int=1,  trackerProcessorNumber:int=1, detectFrameCount:int = 1, scale:int = 1, cfl:int = 200, bufSize:int = 64,
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
                Vision(filter, videoData.width, videoData.height, scale, colors, draw)
            ]
        ]
        pNumbers = []
        pBufSize = [bufSize]
        names = ["StartProcess"]

        if sceneDetector is not None:
            logics[0].append(SceneDetector(sceneDetector))

        if detector is not None:
            logics.append([
                Detector(detector)
            ])
            names.append("DetectProcess")
            pNumbers.append(detectProcessorNumber)
            pBufSize.append(3)

        if tracker is not None:
            logics.append([
                Tracker(tracker, scale, draw)
            ])
            names.append("TrackerProcess")
            pNumbers.append(trackerProcessorNumber)
            pBufSize.append(3)

        if draw:
            logics.append([
                DetectorVisualizer(scale)
            ])
            names.append("Drawers")
            pNumbers.append(1)
            pBufSize.append(3)

        if visionProcessorNumber != 1:
            raise Exception("이거 아직 안만듬 다시 만드셈")
        
        names.append("EndThread")
        pBufSize.append(3)

        flag, receiver, allProcess, allTransmissionMedium = PC.get(logics, pNumbers, compressor, transceiver, pBufSize, names)

        return Loader(videoData, receiver, flag, allProcess, allTransmissionMedium)