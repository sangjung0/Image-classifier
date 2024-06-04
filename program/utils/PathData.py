import pathlib


class PathData:
    """
    특정 파일을 들고오는 클래스
    """
    def __init__(self, path:str, types:list[str]=['.jpg','.jpeg','.png']) -> None:
        path:pathlib.Path = pathlib.Path(path)
        if not path.exists():
            raise Exception("path is not exists")
        if not path.is_dir():
            raise Exception("path is not dir")
        
        self.__path = path
        self.__types = types
    @property
    def path(self) -> pathlib.Path:
        return self.__path
    
    @property
    def types(self) -> list[str]:
        return self.__types.copy()
    
    def __iter__(self):
        return PathData.__PathData(self.path, self.types)
    
    class __PathData:
        def __init__(self, path:pathlib.Path, types:list[str]):
            self.__path = path
            self.__cntIter = iter([])
            self.__types = types

        def __next__(self):
            try:
                return next(self.__cntIter)
            except StopIteration:
                if self.__types:
                    self.__cntIter = self.__path.glob(f'**/*{self.__types.pop()}')
                    return self.__next__()
                else:
                    raise StopIteration