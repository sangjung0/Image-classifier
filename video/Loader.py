from multiprocessing import Value
import cv2
from typing import Type

from project_constants import PROCESSOR_PAUSE, PROCESSOR_RUN, PROCESSOR_STOP
from video.model import Frame
from video.Buffer import Buffer
from util.util import AllProcessIsTerminated, AllTransmissionMediumIsTerminated

class Loader:
    def __init__(self, videoData, buffer:Buffer, flag: Value, lastIndex: Value, isRun: Type[AllProcessIsTerminated], mediumJoin: Type[AllTransmissionMediumIsTerminated.wait]): # type: ignore
        self.__buffer = buffer
        self.__videoData = videoData
        self.__lastIndex = lastIndex
        self.__flag = flag
        self.__videoSectionIter = iter([])
        self.__isRun = isRun
        self.__mediumJoin = mediumJoin

    @property
    def videoData(self):
        return self.__videoData
    
    def isFinish(self):
        if self.__flag.value == PROCESSOR_STOP or self.__isRun.allProcessIsTerminated():
            return True
        return False

    def pause(self):
        self.__flag.value = PROCESSOR_PAUSE

    def stop(self):
        self.__flag.value = PROCESSOR_STOP
        self.__isRun.wait()
        self.__mediumJoin()

    def run(self):
        if self.__flag.value != PROCESSOR_STOP:
            self.__flag.value = PROCESSOR_RUN
        else: raise Exception("프로세서 종료됨")

    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            frame = next(self.__videoSectionIter)
            return PROCESSOR_RUN, True, frame
        except StopIteration:
            section = self.__buffer.get(self.__lastIndex.value)
            if section is None:
                if self.__flag ==  PROCESSOR_STOP:
                    raise StopIteration
                return PROCESSOR_RUN, False, None
            self.__videoSectionIter = iter(section)
            self.__lastIndex.value += 1
            return self.__next__()


            







































    def singleLoader(self):
        frameAry = []
        videoSectionIndex = 0
        videoProcessor = VideoProcessor(VideoSection(-1,[]), self.__detector, self.__tracker, True, self.__sceneDetector)
        width = self.videoData.width
        height = self.videoData.height
        rWidth = width//self.scale
        rHeight = height//self.scale
        delay = int(1000/self.__videoData.fps)
        with self.__videoData as v:
            for index, frame in v:
                if len(frameAry) >= self.__cfl:
                    videoSection = VideoSection(videoSectionIndex, frameAry)
                    frameAry = []
                    videoSectionIndex += 1
                    videoProcessor.videoSection = videoSection
                    print("전처리 완")
                    for f in videoProcessor.processing().frameAry:
                        cv2.imshow(self.fileName, f.getFrame())
                        if cv2.waitKey(delay) & 0xFF == ord('q'):
                            cv2.destroyAllWindows()
                            return 
                    print("로딩")
                
                frameAry.append(Frame(index, frame, width, height, rWidth, rHeight, self.scale, index % self.detectFrameCount == 0, self.__filter))
            
        cv2.destroyAllWindows()