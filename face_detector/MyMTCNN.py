import cv2
from mtcnn import MTCNN
from face_detector.FaceDetector import FaceDetector
from project_constants import FACE, NOSE, EYE, MOUTH

class MyMTCNN(FaceDetector):
    def __init__(self):
        self.mtcnn = MTCNN()

    def detect(self, img, color = cv2.COLOR_BGR2RGB):
        source = self.mtcnn.detect_faces(cv2.cvtColor(img, color))
        boxs = []
        for i in source:
            #얼굴
            boxs.append((
                FACE,
                i['box'][0], 
                i['box'][1],
                i['box'][0] + i['box'][2],
                i['box'][1] + i['box'][3]
            ))
            temp = i['keypoints']
            boxs += [( #코
                NOSE,
                temp['nose'][0] - 1,
                temp['nose'][1] - 1,
                temp['nose'][0] + 1,
                temp['nose'][1] + 1,
            ),( #왼쪽 눈
                EYE,
                temp['left_eye'][0] - 1,
                temp['left_eye'][1] - 1,
                temp['left_eye'][0] + 1,
                temp['left_eye'][1] + 1,
            ),( #오른쪽 눈
                EYE,
                temp['right_eye'][0] - 1,
                temp['right_eye'][1] - 1,
                temp['right_eye'][0] + 1,
                temp['right_eye'][1] + 1,
            ),( #왼쪽 입
                MOUTH,
                temp['mouth_left'][0] - 1,
                temp['mouth_left'][1] - 1,
                temp['mouth_left'][0] + 1,
                temp['mouth_left'][1] + 1,
            ),( #오른쪽 입
                MOUTH,
                temp['mouth_right'][0] - 1,
                temp['mouth_right'][1] - 1,
                temp['mouth_right'][0] + 1,
                temp['mouth_right'][1] + 1,
            )]
        
        return boxs
