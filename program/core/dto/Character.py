class Character:
    """사진에서의 얼굴 위치와 이름을 가지고 있음"""
    def __init__(self, name: int, pos:tuple[int, int] = (0, 0), size:tuple[int, int] = (0, 0)):
        self.name = name
        self.pos = pos
        self.size = size
    
    @property
    def name(self) -> int:
        return self.__name
    
    @name.setter
    def name(self, value:int) -> None:
        if isinstance(value, int):
            self.__name = value
        else: raise TypeError()
    
    @property
    def pos(self) -> tuple[float, float]:
        return self.__pos 
    
    @pos.setter
    def pos(self, value:tuple[float, float]) -> None:
        try:
            self.__pos = (float(value[0]), float(value[1]))
        except Exception as _:
            raise TypeError()
        
    @property
    def size(self) -> tuple[float, float]:
        return self.__size 
    
    @size.setter
    def size(self, value:tuple[float, float]) -> None:
        try:
            self.__size = (float(value[0]), float(value[1]))
        except Exception as _:
            raise TypeError()
