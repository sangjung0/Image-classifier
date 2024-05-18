from multiprocessing.sharedctypes import SynchronizedBase
from pathlib import Path
import cv2

from image_data.logic.StartPointInterface import StartPointInterface

from image_data.model import Section


class Distributor(StartPointInterface):
    """
    이미지를 전달받은 Section에 저장하는 클래스
    """
    def __init__(self, pathData:list[Path], imageSize:tuple, point:SynchronizedBase = None):
        """
        pathData : 이미지 경로가 담긴 배열
        imageSize : 이미지 크기
        point : 특정 이미지부터 로드할때 값을 전달할 변수
        """
        self.__pathList = pathData
        self.__imageSize = imageSize
        self.__point = point

        self.__isLoad = [False for _ in pathData]
        self.__cnt = 0
        self.__step = 0
        self.__setIsFinish = None

    def getPath(self) -> tuple[int, Path]:
        if self.__point and self.__point.value:
            self.__cnt = self.__point.value
            self.__point.value = None
            self.__step = 0
        cnt = self.__cnt
        length = len(self.__pathList)

        while True:
            if self.__step > len(self.__pathList): return -1, None

            temp = cnt + self.__step
            if not self.__isLoad[temp]:
                self.__isLoad[temp] = True
                return (temp + length)%length, self.__pathList[temp]
            
            temp = cnt - self.__step
            if not self.__isLoad[temp]:
                self.__isLoad[temp] = True
                return (temp + length)%length, self.__pathList[temp]

            self.__step += 1

    def prepare(self, setIsFinish:callable) -> None:
        self.__setIsFinish = setIsFinish

    def processing(self, section:Section) -> Section:
        try:
            height, width = self.__imageSize[0:2]
            for i in section:
                i.index, i.path = self.getPath()
                if i.path is None:
                    self.__setIsFinish(True)
                    continue
                img = cv2.imread(str(i.path))
                scale = 1
                imgHeight, imgWidth = img.shape[0:2]
                if imgHeight > height or height > width:
                    if imgHeight/height > imgWidth/width:
                        imgWidth = int(imgWidth/imgHeight * height) 
                        scale = imgHeight/height
                        imgHeight = height
                    else:
                        imgHeight = int(imgHeight/imgWidth * width)
                        scale = imgWidth/width
                        imgWidth = width
                    img = cv2.resize(img, (imgWidth, imgHeight))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                i.sclae = scale
                i.source[:] = 0
                i.source[0:imgHeight, 0:imgWidth] = img
        except Exception as e:
            raise e
        return section
        
