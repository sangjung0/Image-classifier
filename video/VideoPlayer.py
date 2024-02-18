import cv2
from project_constants import STOP
from video.VideoController import VideoController
from video.VideoLoader import VideoLoader
import time
class VideoPlayer:
    def __init__(self, videoLoader:VideoLoader):
        self.__videoLoader = videoLoader

    def play(self):
        self.__videoLoader.run()
        delay = 1000 // self.__videoLoader.videoData.fps
        print("딜레이 :", delay)
        fileName = self.__videoLoader.videoData.fileName
        while True:
            flag, ret, frame = self.__videoLoader.get()
            if ret:
                cv2.imshow(fileName, frame.frame)
            if flag == STOP:
                break
                
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break
        self.__videoLoader.stop()
        cv2.destroyAllWindows()
    