from typing import Type
import cv2
import numpy as np

from face_tracker import TrackerInterface
from video.model import Section, Face
from video.logic import StopOverPointInterface

class Tracker(StopOverPointInterface): #일반 트래커하고 얼굴 트래커하고 나눠보자
    def __init__(self, tracker: Type[TrackerInterface], scale:int, draw:bool) -> None:
        self.__tracker = tracker
        self.__draw = draw
        self.__scale = scale
        self.__colorAry = None
        self.__lines = None
        self.__prevFaces = []

    def prepare(self) -> None:
        self.__tracker = self.__tracker()
        self.__colorAry = np.random.randint(0,255,(self.__tracker.pointNumber,3))
                
    def draw(self, prevPt:list, nextPt:list, frame:np.ndarray) -> None:
        scale = self.__scale
        colorAry = self.__colorAry
        lines = self.__lines
        for i, (p, n) in enumerate(zip(prevPt, nextPt)):
            px, py = map(lambda x : int(x*scale), p)
            nx, ny = map(lambda x: int(x*scale), n)
            cv2.line(lines, (px, py),(nx, ny), colorAry[i].tolist(), 2)
            cv2.circle(frame, (nx, ny), 2, colorAry[i].tolist(), -1)        
        cv2.addWeighted(frame, 1.0, lines, 1.0, 0, frame)

    def clear(self, frame:np.ndarray) -> None:
        self.__lines = np.zeros_like(frame)

    def processing(self, section:Section) -> Section:
        tracker = self.__tracker
        draw = self.__draw

        for frame in section:
            index = frame.index
            prevPt, nextPt = tracker.tracking(frame.getFrame(tracker.colorConstant), frame.isNewScene)
            if nextPt is not None:
                nextPt = list(map(lambda x: tuple(x.ravel()), nextPt))

                faces = frame.face
                for f in faces: #일단 얼굴만 트래킹하자
                    lx,ly,rx,ry = f.face
                    facePoints = f.points
                    for n in nextPt:
                        x,y = n
                        if lx <= x and rx >= x and ly <= y and ry >= y:
                            facePoints.append(n)
                
                if prevPt is not None:
                    prevPt = list(map(lambda x: tuple(x.ravel()), prevPt))
                    pointsDict = dict(zip(prevPt, nextPt))
                    for pf in self.__prevFaces:
                        pfPPoints = pf.points
                        pfNPoints = []
                        for p in pfPPoints:
                            if p in prevPt: pfNPoints.append(pointsDict[p])
                        pfLen = len(pfNPoints)
                        if len(pfNPoints) == 0: continue
                        for f in faces:
                            if len(set(pfNPoints + f.points)) <= pfLen:
                                pf.nextFace = f
                                break
                        else:
                            px, py = zip(*pfPPoints)
                            nx, ny = zip(*pfNPoints)
                            pLen = len(pfPPoints)
                            nLen = len(pfNPoints)
                            px , py = sum(px)/ pLen , sum(py)/pLen
                            nx , ny = sum(nx)/nLen, sum(ny)/nLen
                            dx , dy = nx - px, ny - py
                            temp = lambda lx,ly,rx,ry : (lx + dx, ly + dy, rx + dx, ry + dy)
                            newFace = Face(index, 
                                            temp(*pf.face), 
                                            temp(*pf.nose), 
                                            temp(*pf.lEye), 
                                            temp(*pf.rEye), 
                                            temp(*pf.lMouth), 
                                            temp(*pf.rMouth)
                                            )
                            pf.nextFace = newFace
                            faces.append(newFace) # 구조가 조금 별로움 변경 필요
                
                self.__prevFaces = faces
                        
                if draw:
                    if prevPt is None:
                        self.clear(frame.frame) #만약 그리는게 이상하면 이거 수정
                    else:
                        self.draw(prevPt, nextPt, frame.frame)
            section.compress(frame)
        return section

