import numpy as np
from sklearn.cluster import KMeans as skKMeans
from util.util import Loger, Timer, showImages

class KMeans:
    def __init__(self, faceImgs:np.ndarray, size:tuple):
        self.__original= faceImgs
        self.__arys = self.__original.reshape(-1, size[0]*size[1]*size[2])
        self.__loger = Loger("KMeans")

    def run(self):
        loger = self.__loger
        timer = Timer()

        loger("start", option="start")
        km = skKMeans(n_clusters=3, random_state=0)
        timer.measure(lambda: km.fit(self.__arys))
        loger(np.unique(km.labels_, return_counts=True), option=timer)

        return km.labels_
        
        # loger("1번")
        # ary = self.__original[km.labels_==0]
        # idx = 0
        # while True:
        #     if idx + 100 > len(ary):
        #         showImages(ary[idx: len(ary)])
        #         break
        #     showImages(ary[idx:idx+100])
        #     idx += 100

        # loger("2번")
        # ary = self.__original[km.labels_==1]
        # idx = 0
        # while True:
        #     if idx + 100 > len(ary):
        #         showImages(ary[idx: len(ary)])
        #         break
        #     showImages(ary[idx:idx+100])
        #     idx += 100           

        # loger("3번")
        # ary = self.__original[km.labels_==2]
        # idx = 0
        # while True:
        #     if idx + 100 > len(ary):
        #         showImages(ary[idx: len(ary)])
        #         break
        #     showImages(ary[idx:idx+100])
        #     idx += 100
        
