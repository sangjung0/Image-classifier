class Name:
    def __init__(self):
        self.__names = {}

    def add(self, value:int) -> None:
        self.__names[value] = self.__names.get(value, 0) + 1
    
    def get(self) -> int:
        if self.__names:
            return max(self.__names, key=lambda x:self.__names[x])
        return None
    