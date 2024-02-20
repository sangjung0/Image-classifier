import cv2
import numpy as np
from mtcnn import MTCNN

from face_detector.DetectorInterface import DetectorInterface
from project_constants import DETECTOR_FACE, DETECTOR_FRONT_FACE, DETECTOR_NOSE, DETECTOR_EYE, DETECTOR_MOUTH

class MyMTCNN(DetectorInterface):
    def __init__(self, color = cv2.COLOR_BGR2RGB, min_face_size = 40, margin = 1.2, front = 0.3):
        super().__init__()
        self.__mtcnn = MTCNN(min_face_size=min_face_size)
        self.__color = color
        self.__batch = []
        self.__margin = margin
        self.__front = front

    @property
    def colorConstant(self):
        return self.__color
    
    def batch(self, img: np.ndarray) -> None:
        self.__batch.append(img)
    
    def clear(self) -> None:
        self.__batch.clear()

    def combine(self):
        return np.vstack(tuple(img for img in self.__batch))
    
    def extract(self, scales:list, draw:bool = False, drawFrames:list = None):
        return super()._extract(self.detect(), scales, draw, drawFrames)

    def detect(self):
        margin = self.__margin
        front = self.__front
        length = len(self.__batch)

        source = self.combine()
        height = source.shape[0] // length

        destination = self.__mtcnn.detect_faces(source)
        destination.sort(key=lambda x: x['box'][1] + x['box'][3]//2)

        minHeight = 0
        maxHeight = height
        boxs = []
        imgs = []

        idx = 0
        maxIdx = len(destination)
        while idx < maxIdx:
            f = destination[idx]
            if (f['box'][1] + f['box'][3]//2) > maxHeight:
                imgs.append(boxs)
                boxs = []
                minHeight += height
                maxHeight += height
                continue
            idx+=1

            temp = f['keypoints']

            thrashold = abs(temp['right_eye'][0] - temp['left_eye'][0])//2 * front 
            isFrontFace = temp['nose'][0] - temp['left_eye'][0] > thrashold and temp['right_eye'][0] - temp['nose'][0] > thrashold

            boxs.append(( #얼굴
                DETECTOR_FRONT_FACE if isFrontFace else DETECTOR_FACE,
                f['box'][0] - int(f['box'][2] * ((margin - 1)/2)), 
                f['box'][1] - minHeight - int(f['box'][3] * ((margin - 1)/2)),
                f['box'][0] + int(f['box'][2] * margin),
                f['box'][1] - minHeight + int(f['box'][3] * margin)
            ))

            boxs.append(( #코
                DETECTOR_NOSE,
                temp['nose'][0] - 1,
                temp['nose'][1] - minHeight - 1,
                temp['nose'][0] + 1,
                temp['nose'][1] - minHeight + 1,
            ))

            boxs.append(( #왼쪽 눈
                DETECTOR_EYE,
                temp['left_eye'][0] - 1,
                temp['left_eye'][1] - minHeight - 1,
                temp['left_eye'][0] + 1,
                temp['left_eye'][1] - minHeight + 1,
            ))

            boxs.append(( #오른쪽 눈
                DETECTOR_EYE,
                temp['right_eye'][0] - 1,
                temp['right_eye'][1] - minHeight - 1,
                temp['right_eye'][0] + 1,
                temp['right_eye'][1] - minHeight + 1,
            ))

            boxs.append(( #왼쪽 입
                DETECTOR_MOUTH,
                temp['mouth_left'][0] - 1,
                temp['mouth_left'][1] - minHeight - 1,
                temp['mouth_left'][0] + 1,
                temp['mouth_left'][1] - minHeight + 1,
            ))

            boxs.append(( #오른쪽 입
                DETECTOR_MOUTH,
                temp['mouth_right'][0] - 1,
                temp['mouth_right'][1] - minHeight - 1,
                temp['mouth_right'][0] + 1,
                temp['mouth_right'][1] - minHeight + 1,
            ))

        for _ in range(length - len(imgs)):
            imgs.append([])
        return imgs
