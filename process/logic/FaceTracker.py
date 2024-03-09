from process.logic.StopOverPointInterface import StopOverPointInterface

from process.model import Section, Face

class FaceTracker(StopOverPointInterface): #일반 트래커하고 얼굴 트래커하고 나눠보자
    def __init__(self) -> None:
        self.__prevFaces = []

    def prepare(self) -> None:
        return

    def processing(self, section:Section) -> Section:

        for frame in section:
            if frame.isNewScene:
                self.__prevFaces.clear()
            index = frame.index
            prevPt, nextPt = frame.points

            if nextPt is not None:
                faces = frame.face
                for f in faces: #일단 얼굴만 트래킹하자
                    lx,ly,rx,ry = f.face
                    facePoints = f.points
                    for n in nextPt:
                        x,y = n
                        if lx <= x and rx >= x and ly <= y and ry >= y:
                            facePoints.append(n)
                
                if prevPt is not None:
                    pointsDict = dict(zip(prevPt, nextPt))
                    for pf in self.__prevFaces:
                        pfPPoints = pf.points
                        pfNPoints = []
                        for p in pfPPoints:
                            if p in prevPt: pfNPoints.append(pointsDict[p])
                        pfLen = len(pfNPoints)
                        if pfLen == 0: continue
                        for f in faces:
                            if len(set(pfNPoints + f.points)) <= pfLen + 20:
                                pf.nextFace = f
                                break
                        else:
                            px, py = zip(*pfPPoints)
                            nx, ny = zip(*pfNPoints)
                            pLen = len(pfPPoints)
                            nLen = len(pfNPoints)
                            px , py = sum(px)/ pLen , sum(py)/pLen
                            nx , ny = sum(nx)/nLen, sum(ny)/nLen
                            dx , dy = int(nx - px), int(ny - py)
                            fd = {}
                            for k in pf.faceData:
                                lx, ly, rx, ry = pf.faceData[k]
                                fd[k] = (lx + dx, ly + dy, rx + dx, ry + dy)
                            newFace = Face(index, fd)
                            newFace.points = pfNPoints
                            pf.nextFace = newFace
                            faces.append(newFace) # 구조가 조금 별로움 변경 필요
                self.__prevFaces = faces
            
            frame.points = (prevPt, nextPt)
        return section

