import numpy as np

from core.dto import Face
from core.scheduler.processor.Processor import Processor
from core.scheduler.dto import Packet

from core.Constant import FACE_CLASSIFIER_MAX_FACE, FACE_CLASSIFIER_THRESHOLD

class FaceClassifier(Processor):
    """얼굴 분류하는 멀티프로세싱의 기반이 되는 클래스"""
    
    def __init__(self, name:str, faces:dict[int:list[Face]],loger_is_print:bool = False) -> None:
        super().__init__(name, loger_is_print)
        self.__faces:dict[int:list[Face]] = faces
    
    def compare(self, embedding_1:np.ndarray, embedding_2:np.ndarray) -> bool:
        return np.linalg.norm(embedding_1 - embedding_2) < FACE_CLASSIFIER_THRESHOLD
    
    def set_face(self, n: int, face: Face) -> None:
        self.__faces[n].append(face)
        if(len(self.__faces[n]) > FACE_CLASSIFIER_MAX_FACE):
            self.__faces[n].pop(0)
            
    def processing(self, value:Packet) -> Packet:
        
        for p in value:
            if p.path == None: break
            for face, character in zip(p.faces.values(), p.characters.values()):
                name = [0 for _ in range(len(self.__faces))]
                embedding = face.embedding
                
                for i, l in enumerate(self.__faces.values()):
                    for f in l:
                        if self.compare(embedding, f.embedding):
                            name[i] += 1

                id = 0
                for i in range(len(name)):
                    if name[i] > name[id]: id = i
                    
                if len(self.__faces) == 0 or name[id] == 0:
                    id = len(self.__faces)
                    self.__faces[id] = [face]
                else:
                    self.set_face(id, face)
                
                face.name = id
                character.name = id
        
        return value