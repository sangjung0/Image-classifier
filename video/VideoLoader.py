from multiprocessing import Queue, Value
import cv2
import bisect
import pickle

from project_constants import PAUSE, RUN, STOP
from video.model import Frame
from video.model import VideoSection
from video.VideoProcessor import VideoProcessor

class VideoLoader:
    def __init__(self, videoData, result:Queue, isFinish:object, flag: Value, lastIndex: Value): # type: ignore
        self.__videoData = videoData
        self.__result =result
        self.__isFinish = isFinish
        self.__lastIndex = lastIndex
        self.__flag = flag
        self.__videoSections = []
        self.__frames = []
        self.__index = 0

    @property
    def videoData(self):
        return self.__videoData

    def pause(self):
        self.__flag.value = PAUSE

    def stop(self):
        self.__flag.value = STOP

    def run(self):
        if self.__flag.value != STOP:
            self.__flag.value = RUN
        else: raise Exception("프로세서 종료됨")

    def getVideoSection(self):
        if self.__result.empty():
            if self.__isFinish():
                return False, None
        else:
            videoSection = pickle.loads(self.__result.get())
            print(videoSection.index, "받음")
            if videoSection.index == self.__lastIndex.value:
                return True, videoSection
            bisect.insort(self.__videoSections, videoSection)
        if len(self.__videoSections) > 0 and self.__videoSections[0].index == self.__lastIndex.value:
            return True, self.__videoSections.pop(0)
        return True, None

    def getFrame(self):
        if len(self.__frames) == self.__index:
            ret, videoSection = self.getVideoSection()
            if ret:
                if videoSection is None:
                    return RUN, False, None
                self.__frames = videoSection.frames
                self.__index = 0
                print(self.__lastIndex.value, "완료")
                self.__lastIndex.value += 1
            else:
                return STOP, False, None
        frame = self.__frames[self.__index]
        self.__index += 1
        return RUN, True, frame


            







































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