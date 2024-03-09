from process.logic.StopOverPointInterface import StopOverPointInterface

from process.model import Section, Face

class InsertFace(StopOverPointInterface):
    def __init__(self, faces:list[Face]) -> None:
        self.__faces = faces
        self.__idx = 0

    def prepare(self) -> None:
        return
    
    def processing(self, section: Section) -> Section:
        faces = self.__faces
        for frame in section:
            while True:
                if self.__idx < len(faces) and faces[self.__idx].frameIndex == frame.index:
                    frame.face.append(faces[self.__idx])
                    self.__idx += 1
                else: break
        
        return section