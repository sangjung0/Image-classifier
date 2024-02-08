import cv2

class VideoData:
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
        
    def play(self, function = None):
        if(self.fileName is None): raise Exception("파일 이름 없음")
        cap = VideoData.read(self.fileName)
        delay = int(1000/cap.get(cv2.CAP_PROP_FPS))
        while(cap.isOpened()):
            ret, frame = cap.read()

            if ret:
                if function is not None:
                    lx, ly, rx, ry, color, weight = function(frame)
                    cv2.rectangle(frame, (lx, ly), (rx, ry), color, weight)
                cv2.imshow(self.fileName, frame)

            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    @staticmethod
    def read(fileName):
        return cv2.VideoCapture(fileName)
