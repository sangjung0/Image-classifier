from multiprocessing import Value
from project_constants import PAUSE, RUN, STOP
from video.VideoBuffer import VideoBuffer
from video.Frame import Frame
from video.VideoSection import VideoSection
from video.VideoProcessor import VideoProcessor
import cv2

class VideoLoader:
    def __init__(self, videoBuffer: VideoBuffer, flag: Value, lastIndex): # type: ignore
        self.__videoBuffer = videoBuffer
        self.__lastIndex = lastIndex
        self.__flag = flag
        self.__frames = []
        self.__index = 0

    def pause(self):
        self.__flag.value = PAUSE

    def stop(self):
        self.__flag.value = STOP

    def run(self):
        if self.__flag.value != STOP:
            self.__flag.value = RUN
        else: raise Exception("프로세서 종료됨")

    def get(self):
        try:
            if len(self.__frames) == self.__index:
                videoSection = self.__videoBuffer.get(self.__lastIndex.value+1)
                self.__frames = videoSection.frameAry
                self.__index = 0
                print(self.__lastIndex.value, "완료")
                self.__lastIndex.value = videoSection.index
            frame = self.__frames.pop(self.__index)
            self.__index += 1
            return RUN, True, frame
        except Exception as err:
            if self.__flag == STOP:
                return STOP, False, None
            elif self.__flag == PAUSE:
                return PAUSE, False, None
            else:
                return RUN, False, None


            







































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