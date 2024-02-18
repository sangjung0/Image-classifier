from multiprocessing import Process, Queue, Value
from threading import Thread

from video.VideoBuffer import VideoBuffer
from video.VideoData import VideoData
from video.VideoData import VideoData
from video.VideoLoader import VideoLoader
from video.VideoProcessor import VideoProcessor
from video.VideoDistributor import VideoDistributor
from project_constants import PAUSE
from util.util import AllProcessIsTerminated, AllTransmissionMediumIsTerminated
from util.compressor import CompressorInterface, UnCompressor
from util.serializer import PickleSerializer
from util.transceiver import TransceiverInterface, Transceiver

class VideoController:

    @staticmethod
    def startAndGetVideoLoader(
        fileName:str, processorNumber:int = 3, detectFrameCount:int = 1, scale:int = 1, cfl:int = 50, bufSize:int = 5,
        transceiver:TransceiverInterface = Transceiver(PickleSerializer(), UnCompressor()), compressor: CompressorInterface = None,
        filter = None, detector = None, tracker = None, sceneDetector = None, draw:bool = False
        ):

        videoData = VideoData(fileName)
        videoBuffer = VideoBuffer()
        processes = []
        data = Queue()
        result = Queue()
        flag = Value('i',PAUSE)
        lastIndex = Value('i', 0)

        videoDistributorProcess = Process(target=VideoDistributor(videoData, scale, detectFrameCount, cfl, bufSize, filter), args=(data, flag, lastIndex, transceiver, compressor))
        videoDistributorProcess.start()

        for _ in range(processorNumber):
            p = Process(target=VideoProcessor(detector, tracker, sceneDetector, draw), args=(data, result, flag, transceiver))
            p.start()
            processes.append(p)

        videoBufferThread = Thread(target=videoBuffer, args=(result, flag, AllProcessIsTerminated(processes).allProcessIsTerminated, transceiver))
        videoBufferThread.start()

        return VideoLoader(
            videoData, videoBuffer, flag, lastIndex, 
            AllProcessIsTerminated(processes+[videoDistributorProcess, videoBufferThread]).wait,
            AllTransmissionMediumIsTerminated([data,result]).wait
            )