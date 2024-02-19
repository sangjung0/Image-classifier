import cv2
from mtcnn import MTCNN

from face_detector.DetectorInterface import DetectorInterface
from project_constants import DETECTOR_FACE, DETECTOR_NOSE, DETECTOR_EYE, DETECTOR_MOUTH

class MyMTCNN(DetectorInterface):
    def __init__(self, color = cv2.COLOR_BGR2RGB):
        super().__init__()
        self.__mtcnn = MTCNN()
        self.__color = color

    @property
    def colorConstant(self):
        return self.__color
    
    def extract(self, img, draw = False, drawFrame = None, scale = None):
        super().extract(self.detect(img), draw, drawFrame, scale)

    def detect(self, img):
        source = self.__mtcnn.detect_faces(img)
        boxs = []
        for i in source:
            #얼굴
            boxs.append((
                DETECTOR_FACE,
                i['box'][0], 
                i['box'][1],
                i['box'][0] + i['box'][2],
                i['box'][1] + i['box'][3]
            ))
            temp = i['keypoints']
            boxs += [( #코
                DETECTOR_NOSE,
                temp['nose'][0] - 1,
                temp['nose'][1] - 1,
                temp['nose'][0] + 1,
                temp['nose'][1] + 1,
            ),( #왼쪽 눈
                DETECTOR_EYE,
                temp['left_eye'][0] - 1,
                temp['left_eye'][1] - 1,
                temp['left_eye'][0] + 1,
                temp['left_eye'][1] + 1,
            ),( #오른쪽 눈
                DETECTOR_EYE,
                temp['right_eye'][0] - 1,
                temp['right_eye'][1] - 1,
                temp['right_eye'][0] + 1,
                temp['right_eye'][1] + 1,
            ),( #왼쪽 입
                DETECTOR_MOUTH,
                temp['mouth_left'][0] - 1,
                temp['mouth_left'][1] - 1,
                temp['mouth_left'][0] + 1,
                temp['mouth_left'][1] + 1,
            ),( #오른쪽 입
                DETECTOR_MOUTH,
                temp['mouth_right'][0] - 1,
                temp['mouth_right'][1] - 1,
                temp['mouth_right'][0] + 1,
                temp['mouth_right'][1] + 1,
            )]
        
        return boxs
