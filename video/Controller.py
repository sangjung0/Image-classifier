from multiprocessing import Process, Queue, Value
from threading import Thread
from typing import Type

from video.Buffer import Buffer
from video.VideoData import VideoData
from video.VideoData import VideoData
from video.Loader import Loader
from video.processor import *
from video.Distributor import Distributor
from project_constants import PROCESSOR_PAUSE
from util.util import AllProcessIsTerminated, AllTransmissionMediumIsTerminated
from util.compressor import CompressorInterface, UnCompressor
from util.serializer import PickleSerializer
from util.transceiver import TransceiverInterface, Transceiver
from face_detector import DetectorInterface
from face_tracker import TrackerInterface

class Controller:

    @staticmethod
    def startAndGetVideoLoader(
        fileName:str, visionProcessorNumber:int = 1, detectProcessorNumber:int=1,  trackerProcessorNumber:int=1, detectFrameCount:int = 1, scale:int = 1, cfl:int = 200, bufSize:int = 64,
        transceiver:TransceiverInterface = Transceiver(PickleSerializer(), UnCompressor()), compressor: Type[CompressorInterface] = None,
        filter = None, detector:Type[DetectorInterface] = None, tracker:Type[TrackerInterface] = None, sceneDetector:Type[object] = None, draw:bool = False
        ):

        videoData = VideoData(fileName)
        colors = set()

        if detector is not None: colors.add(detector.COLOR)
        if tracker is not None: colors.add(tracker.COLOR)
        
        visionProcessors = []
        detectProcessors = []
        trackerProcessors = []
        
        distributorToVision = Queue()
        visionToDetector = Queue()
        detectorToTracker = Queue()
        result = Queue()
        flag = Value('i',PROCESSOR_PAUSE)
        lastIndex = Value('i', 0)

        distributor = Distributor(videoData, detectFrameCount, cfl, bufSize)
        vision = VisionProcessor(filter, sceneDetector, videoData.width, videoData.height, scale, colors, draw)
        detector_ = DetectProcessor(detector, scale, draw)
        tracker_ = TrackerProcessor(tracker, scale, draw)
        buffer = Buffer()
    
        videoDistributorProcess = Process(
            target=distributor, 
            args=(distributorToVision, flag, lastIndex, transceiver, compressor)
            )
        videoDistributorProcess.start()

        for _ in range(visionProcessorNumber):
            p = Process(
                target=vision, 
                args=(
                    distributorToVision, visionToDetector, flag, transceiver
                    )
                )
            p.start()
            visionProcessors.append(p)

        for _ in range(detectProcessorNumber):
            p = Process(
                target=detector_,
                args=(
                    visionToDetector, detectorToTracker, flag, transceiver
                )
            )
            p.start()
            detectProcessors.append(p)

        for _ in range(trackerProcessorNumber):
            p = Process(
                target=tracker_,
                args=(
                    detectorToTracker, result, flag, transceiver
                )
            )
            p.start()
            trackerProcessors.append(p)


        videoBufferThread = Thread(target=buffer, args=(result, flag, AllProcessIsTerminated(trackerProcessors).allProcessIsTerminated, transceiver))
        videoBufferThread.start()

        return Loader(
            videoData, buffer, flag, lastIndex, 
            AllProcessIsTerminated(visionProcessors + detectProcessors + trackerProcessors +[videoDistributorProcess, videoBufferThread]),
            AllTransmissionMediumIsTerminated([distributorToVision, visionToDetector, detectorToTracker, result]).wait
            )