import cv2
from project_constants import STOP
from video.VideoController import VideoController
from video.VideoLoader import VideoLoader
import time

class VideoPlayer:
    def __init__(self, videoController:VideoController, videoLoader:VideoLoader):
        self.__videoLoader = videoLoader
        self.__videoController = videoController

    def play(self):
        self.__videoLoader.run()
        delay = int(1000 / self.__videoController.videoData.fps)
        print("딜레이 :", delay)
        fileName = self.__videoController.videoData.fileName
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
    