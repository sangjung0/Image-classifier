from multiprocessing import Process, Queue, Value
from threading import Thread
from typing import Type

from video.Buffer import Buffer
from video.VideoData import VideoData
from video.VideoData import VideoData
from video.Loader import Loader
from video.processor.VisionProcessor import VisionProcessor
from video.processor.DetectProcessor import DetectProcessor
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
        fileName:str, visionProcessorNumber:int = 1, detectProcessorNumber:int=1,  detectFrameCount:int = 1, scale:int = 1, cfl:int = 50, bufSize:int = 64,
        transceiver:TransceiverInterface = Transceiver(PickleSerializer(), UnCompressor()), compressor: Type[CompressorInterface] = None,
        filter = None, detector:Type[DetectorInterface] = None, tracker:Type[TrackerInterface] = None, sceneDetector:Type[object] = None, draw:bool = False
        ):

        videoData = VideoData(fileName)
        buffer = Buffer()
        visionProcessors = []
        detectProcessors = []
        distributorToVision = Queue()
        visionToDetector = Queue()
        result = Queue()
        flag = Value('i',PROCESSOR_PAUSE)
        lastIndex = Value('i', 0)

        videoDistributorProcess = Process(
            target=Distributor(videoData, scale, detectFrameCount, cfl, bufSize, filter), 
            args=(distributorToVision, flag, lastIndex, transceiver, compressor)
            )
        videoDistributorProcess.start()

        for _ in range(visionProcessorNumber):
            p = Process(
                target=VisionProcessor(tracker, sceneDetector, draw), 
                args=(
                    distributorToVision, visionToDetector, flag, transceiver, 
                    AllProcessIsTerminated([videoDistributorProcess]).allProcessIsTerminated
                    )
                )
            p.start()
            visionProcessors.append(p)

        for _ in range(detectProcessorNumber):
            p = Process(
                target=DetectProcessor(detector, draw),
                args=(
                    visionToDetector, result, flag, transceiver,
                    AllProcessIsTerminated(visionProcessors).allProcessIsTerminated,
                )
            )
            p.start()
            detectProcessors.append(p)

        videoBufferThread = Thread(target=buffer, args=(result, flag, AllProcessIsTerminated(detectProcessors).allProcessIsTerminated, transceiver))
        videoBufferThread.start()

        return Loader(
            videoData, buffer, flag, lastIndex, 
            AllProcessIsTerminated(visionProcessors + detectProcessors +[videoDistributorProcess, videoBufferThread]).wait,
            AllTransmissionMediumIsTerminated([distributorToVision, visionToDetector, result]).wait
            )