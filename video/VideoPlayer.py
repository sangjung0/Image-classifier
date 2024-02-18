import cv2
from project_constants import STOP
from video.VideoController import VideoController
from video.VideoLoader import VideoLoader
class VideoPlayer:
    def __init__(self, videoLoader:VideoLoader):
        self.__videoLoader = videoLoader

    def play(self):
        self.__videoLoader.run()
        delay = 1000 // self.__videoLoader.videoData.fps
        print("딜레이 :", delay)
        fileName = self.__videoLoader.videoData.fileName
        for flag, ret, frame in self.__videoLoader:
            if ret:
                cv2.imshow(fileName, frame.frame)
            if flag == STOP: # Stop 처리는 안해도 될 듯
                break
                
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        self.__videoLoader.stop()
        return
    