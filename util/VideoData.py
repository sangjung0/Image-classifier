import cv2
import numpy as np

class VideoData:    
    def __init__(self, fileName = None, detectFrame = 1, scale = 1):
        self.fileName = fileName
        self.__detectFrame = detectFrame
        self.__scale = scale

    @property
    def fileName(self):
        return self.__fileName
    
    @fileName.setter
    def fileName(self, value):
        if value.strip() != '':
            self.__fileName = value
        else: raise Exception("fileName 값 잘못 됨")
        
    def play(self, detector = None, filter = None, tracker = None, sceneDetector = None):
        if(self.fileName is None): raise Exception("파일 이름 없음")

        cap = VideoData.read(self.fileName)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        delay = int(1000/cap.get(cv2.CAP_PROP_FPS))
        count = 0

        while(cap.isOpened()):
            ret, frame = cap.read()
            if count % self.__detectFrame == 0:
                count = 0

            if ret:
                resizedFrame = cv2.resize(frame, (width//self.__scale, height//self.__scale))
                img = filter(resizedFrame) if filter is not None else resizedFrame
                isNewScene = sceneDetector.isNewScene(img) if sceneDetector else False

                if detector is not None and (count == 0 or isNewScene):
                    faceLocation = detector.detect(img, draw=True, drawFrame=frame)

                if tracker is not None:
                    trackingData = tracker.tracking(img, isNewScene=isNewScene, draw=True, drawFrame=frame)

                cv2.imshow(self.fileName, frame)
            count += 1

            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    @staticmethod
    def read(fileName):
        return cv2.VideoCapture(fileName)
