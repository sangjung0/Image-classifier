import cv2
import numpy as np
from mtcnn import MTCNN

from process.face_detector.DetectorInterface import DetectorInterface

from project_constants import DETECTOR_FACE, DETECTOR_NOSE, DETECTOR_LEFT_EYE, DETECTOR_LEFT_MOUTH, DETECTOR_RIGHT_EYE, DETECTOR_RIGHT_MOUTH

class MyMTCNN(DetectorInterface):
    COLOR = cv2.COLOR_BGR2RGB

    def __init__(self, color:int = COLOR, min_face_size:int = 20) -> None:
        super().__init__()
        self.__mtcnn = MTCNN(min_face_size=min_face_size)
        self.__color = color
        self.__batch:list[np.ndarray] = []

    @property
    def colorConstant(self) -> int:
        return self.__color
    
    def batch(self, img: np.ndarray) -> None:
        self.__batch.append(img)
    
    def clear(self) -> None:
        self.__batch.clear()

    def combine(self) -> np.ndarray:
        maxWidth = max(self.__batch, key= lambda x:x.shape[1]).shape[1]
        temp = []
        for img in self.__batch:
            padding = np.zeros((img.shape[0], maxWidth - img.shape[1], img.shape[2]))
            temp.append(np.hstack((img, padding)))

        return np.vstack(tuple(img for img in temp))

    def detect(self) -> list[list[dict[int,tuple[int,int,int,int]]]]:
        destination = self.__mtcnn.detect_faces(self.combine())
        destination.sort(key=lambda x: x['box'][1] + x['box'][3]//2)

        if not destination: return []

        imgsFaces = []
        desIter = iter(destination)
        f = next(desIter)
        minHeight = 0
        maxHeight = 0
        height = 0
        for img in self.__batch:
            faces = []
            minHeight += height
            height = img.shape[0]
            maxHeight += height
            while desIter:
                try:
                    if f['box'][1] + f['box'][3]/2 > maxHeight:
                        imgsFaces.append(faces)
                        break
                    face = {}
                    temp = f['keypoints']

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
                    faces.append(face)
                    f = next(desIter)
                except StopIteration:
                    break

        return imgsFaces
