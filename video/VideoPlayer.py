from video.VideoData import VideoData
from video.Frame import Frame
from video.VideoSection import VideoSection
from video.VideoProcessor import VideoProcessor
import cv2

class VideoPlayer:
    def __init__(self, fileName:str, detectFrameCount:int = 1, scale:int = 1, cfl = 1000, filter = None, detector = None, tracker = None, sceneDetector = None ) -> None:
        self.__videoData = VideoData(fileName)
        self.detectFrameCount = detectFrameCount
        self.scale = scale
        self.__cfl = cfl
        self.__filter = filter
        self.__detector = detector
        self.__tracker = tracker
        self.__sceneDetector = sceneDetector

    @property
    def videoData(self):
        return self.__videoData  
    @videoData.setter
    def videoData(self, value):
        if isinstance(value, VideoData):
            self.__videoData = value
        else: raise ValueError("VideoData must be VideoData instance")
    
    @property
    def fileName(self):
        return self.__videoData.fileName
    @fileName.setter
    def fileName(self, value):
        self.__videoData.fileName = value

    @property
    def detectFrameCount(self):
        return self.__detectFrameCount
    @detectFrameCount.setter
    def detectFrameCount(self, value):
        if isinstance(value, int) and value > 0:
            self.__detectFrameCount = value
        else: raise Exception("detectFrame 값 잘못 됨")
    @property
    def scale(self):
        return self.__scale
    @scale.setter
    def scale(self, value):
        if isinstance(value, int) and value > 0:
            self.__scale = value
        else: raise Exception("scale 값 잘못 됨")
        self.__videoData.scale = value

    def singleProcessPlay(self):
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