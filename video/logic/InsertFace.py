from video.logic.StopOverPointInterface import StopOverPointInterface

from video.model import Section, Face

class InsertFace(StopOverPointInterface):
    def __init__(self, faces:list[Face]) -> None:
        self.__faces = faces
        self.__faces.reverse()

    def prepare(self) -> None:
        return
    
    def processing(self, section: Section) -> Section:
        faces = self.__faces
        for frame in section:
            if faces and faces[-1].frameIndex == frame.index:
                frame.face.append(faces.pop())
        
        return section