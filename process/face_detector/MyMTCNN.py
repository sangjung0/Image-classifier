import cv2
import numpy as np
from mtcnn import MTCNN

from process.face_detector.DetectorInterface import DetectorInterface

from project_constants import DETECTOR_FACE, DETECTOR_NOSE, DETECTOR_LEFT_EYE, DETECTOR_LEFT_MOUTH, DETECTOR_RIGHT_EYE, DETECTOR_RIGHT_MOUTH

class MyMTCNN(DetectorInterface):
    COLOR = cv2.COLOR_BGR2RGB

    def __init__(self, color = COLOR, min_face_size = 40):
        super().__init__()
        self.__mtcnn = MTCNN(min_face_size=min_face_size)
        self.__color = color
        self.__batch = []

    @property
    def colorConstant(self):
        return self.__color
    
    def batch(self, img: np.ndarray) -> None:
        self.__batch.append(img)
    
    def clear(self) -> None:
        self.__batch.clear()

    def combine(self):
        return np.vstack(tuple(img for img in self.__batch))

    def detect(self):
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
            face = {}
            temp = f['keypoints']

            # thrashold = abs(temp['right_eye'][0] - temp['left_eye'][0])//2 * front 
            # isFrontFace = temp['nose'][0] - temp['left_eye'][0] > thrashold and temp['right_eye'][0] - temp['nose'][0] > thrashold
            #DETECTOR_FRONT_FACE if isFrontFace else DETECTOR_FACE
            face[DETECTOR_FACE] = ( #얼굴
                f['box'][0], 
                f['box'][1] - minHeight,
                f['box'][0] + f['box'][2],
                f['box'][1] - minHeight + f['box'][3]
            )

            face[DETECTOR_NOSE] = ( #코
                temp['nose'][0] - 1,
                temp['nose'][1] - minHeight - 1,
                temp['nose'][0] + 1,
                temp['nose'][1] - minHeight + 1,
            )

            face[DETECTOR_LEFT_EYE] = ( #왼쪽 눈
                temp['left_eye'][0] - 1,
                temp['left_eye'][1] - minHeight - 1,
                temp['left_eye'][0] + 1,
                temp['left_eye'][1] - minHeight + 1,
            )

            face[DETECTOR_RIGHT_EYE]=(#오른쪽 눈
                temp['right_eye'][0] - 1,
                temp['right_eye'][1] - minHeight - 1,
                temp['right_eye'][0] + 1,
                temp['right_eye'][1] - minHeight + 1,
            )

            face[DETECTOR_LEFT_MOUTH]=( #왼쪽 입
                temp['mouth_left'][0] - 1,
                temp['mouth_left'][1] - minHeight - 1,
                temp['mouth_left'][0] + 1,
                temp['mouth_left'][1] - minHeight + 1,
            )

            face[DETECTOR_RIGHT_MOUTH] = ( #오른쪽 입
                temp['mouth_right'][0] - 1,
                temp['mouth_right'][1] - minHeight - 1,
                temp['mouth_right'][0] + 1,
                temp['mouth_right'][1] - minHeight + 1,
            )
            boxs.append(face)

        for _ in range(length - len(imgs)):
            imgs.append([])
        return imgs
