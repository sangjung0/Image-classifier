import cv2

from video.Loader import Loader

from project_constants import PROCESSOR_STOP

class VideoPlayer:
    def __init__(self, Loader:Loader):
        self.__loader = Loader

    def play(self):
        self.__loader.run()
        delay = 1000 // self.__loader.videoData.fps
        print("딜레이 :", delay)
        fileName = self.__loader.videoData.fileName
        for flag, ret, frame in self.__loader:
            if ret:
                cv2.imshow(fileName, frame.frame)
            elif flag == PROCESSOR_STOP: # Stop 처리는 안해도 될 듯
                break
                
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        self.__loader.stop()
        return