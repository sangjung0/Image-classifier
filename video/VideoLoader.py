from multiprocessing import Value
import cv2

from project_constants import PAUSE, RUN, STOP
from video.model import Frame, VideoSection
from video.VideoBuffer import VideoBuffer
from video.VideoProcessor import VideoProcessor

class VideoLoader:
    def __init__(self, videoData, videoBuffer:VideoBuffer, flag: Value, lastIndex: Value, join:object, mediumJoin:object): # type: ignore
        self.__videoBuffer = videoBuffer
        self.__videoData = videoData
        self.__lastIndex = lastIndex
        self.__flag = flag
        self.__frames = []
        self.__index = 0
        self.__join = join
        self.__mediumJoin = mediumJoin

    @property
    def videoData(self):
        return self.__videoData

    def pause(self):
        self.__flag.value = PAUSE

    def stop(self):
        self.__flag.value = STOP
        self.__mediumJoin()
        print("모든 전송매체 종료")
        self.__join()
        print("모든 프로세서 종료")

    def run(self):
        if self.__flag.value != STOP:
            self.__flag.value = RUN
        else: raise Exception("프로세서 종료됨")

    def get(self):
        if len(self.__frames) == self.__index:
            if self.__flag ==  STOP:
                return STOP, False, None
            videoSection = self.__videoBuffer.get(self.__lastIndex.value)
            if videoSection is None:
                return RUN, False, None
            self.__frames = videoSection.frames
            self.__index = 0
            print(self.__lastIndex.value, "완료")
            self.__lastIndex.value += 1
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