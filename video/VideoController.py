from multiprocessing import Process, Queue, Value
import pickle
from threading import Thread
import time

from video.VideoBuffer import VideoBuffer
from video.model import Frame
from video.VideoData import VideoData
from video.model.VideoSection import VideoSection
from video.VideoData import VideoData
from video.VideoLoader import VideoLoader
from video.VideoProcessor import VideoProcessorGenerator
from project_constants import STOP, RUN, PAUSE, END_OF_LOAD
from util.util import AllProcessIsTerminated

class VideoController:

    @staticmethod
    def startAndGetVideoLoader(fileName:str, processorNumber:int = 4, detectFrameCount:int = 1, scale:int = 1, cfl:int = 50, filter = None, detector = None, tracker = None, sceneDetector = None, draw:bool = False):

        videoData = VideoData(fileName)
        videoBuffer = VideoBuffer()
        processes = []
        videoProcessorGenerator = VideoProcessorGenerator(detector, tracker, sceneDetector, draw).generate
        data = Queue()
        result = Queue()
        flag = Value('i',PAUSE)
        lastIndex = Value('i', 0)

        Process(target=VideoController.__videoDistributor, args=(data, flag, lastIndex, videoData, scale, detectFrameCount, cfl, filter)).start()

        for _ in range(processorNumber):
            p = Process(target=videoProcessorGenerator(), args=(data, result, flag))
            p.start()
            processes.append(p)

        Thread(target=videoBuffer, args=(result, flag, AllProcessIsTerminated(processes).allProcessIsTerminated)).start()

        return VideoLoader(videoData, videoBuffer, flag, lastIndex)

    @staticmethod
    def __videoDistributor(data: Queue, flag: Value, lastIndex: Value, videoData:VideoData, scale:int, detectFrameCount:int, cfl, filter): # type: ignore
        frameAry = []
        videoSectionIndex = 0

        frameGenerator = Frame.FrameGenerator(
            videoData.width, videoData.height, scale, filter,
            lambda x: x % detectFrameCount == 0, 
        ).generate

        with videoData as v:
            it = iter(v)
            while True:
                if flag.value == RUN:
                    if videoSectionIndex - lastIndex.value < 5:
                        try:
                            index, frame = next(it)
                            frameAry.append(frameGenerator(index, frame))
                            if len(frameAry) >= cfl:
                                data.put(pickle.dumps(VideoSection(videoSectionIndex, frameAry)))
                                frameAry.clear()
                                print(videoSectionIndex, "보냄")
                                videoSectionIndex += 1
                        except StopIteration:
                            break
                elif flag.value == PAUSE:
                    time.sleep(0.5)
                elif flag.value == STOP:
                    print("영상 로드 프로세서 종료")
                    return
        print("영상 로드 종료")
        flag.value = END_OF_LOAD