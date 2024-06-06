import numpy as np


class Face:
    """
    얼굴의 이름 번호와 이미지 데이터를 가지고 있음
    """
    def __init__(self, name: int, embedding: np.ndarray): 
        self.name = name
        self.embedding = embedding
        
    @property
    def name(self) -> int:
        return self.__name
    
    @name.setter
    def name(self, value:int) -> None:
        if isinstance(value, int):
            self.__name = value
        else: raise TypeError() 
    
    @property
    def embedding(self) -> np.ndarray:
        return self.__embedding
    
    @embedding.setter
    def embedding(self, value:np.ndarray) -> None:
        if isinstance(value, np.ndarray):
            self.__embedding = value
        else: raise TypeError() 


