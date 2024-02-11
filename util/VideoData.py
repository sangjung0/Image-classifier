import cv2
from project_constants import FACE, NOSE, MOUTH, EYE

class VideoData:
    __COLORS = {
        FACE : (255, 0, 0),
        NOSE : (0, 255, 0),
        MOUTH : (0, 0, 255),
        EYE : (255,255,0)
    }
    __WEIGHT = {
        FACE : 3,
        NOSE : 3,
        MOUTH : 3,
        EYE : 3
    }
    
    def __init__(self, fileName = None):
        self.fileName = fileName

    @property
    def fileName(self):
        return self.__fileName
    
    @fileName.setter
    def fileName(self, value):
        if value.strip() != '':
            self.__fileName = value
        else: raise Exception("fileName 값 잘못 됨")
        
    def play(self, detector = None, filter = None, tracking = None, isNewScene = None):
        if(self.fileName is None): raise Exception("파일 이름 없음")
        cap = VideoData.read(self.fileName)
        delay = int(1000/cap.get(cv2.CAP_PROP_FPS))
        while(cap.isOpened()):
            ret, frame = cap.read()

            if ret:
                img = filter(frame) if filter is not None else frame
                if detector is not None:
                    for kind, lx, ly, rx, ry in detector(img):
                        cv2.rectangle(frame, (lx, ly), (rx, ry), VideoData.__COLORS[kind], VideoData.__WEIGHT[kind])
                if tracking is not None:
                    tracking(img, isNewScene(img) if isNewScene else False)
                cv2.imshow(self.fileName, frame)

            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    @staticmethod
    def read(fileName):
        return cv2.VideoCapture(fileName)
