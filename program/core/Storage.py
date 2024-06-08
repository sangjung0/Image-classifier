import pathlib
import pickle

from core.dto import Data


class Storage:
    def __init__(self, path:pathlib.Path):
        self.__path: pathlib.Path = path
        self.__data: Data = None

    def save(self) -> None:
        if self.__data is not None:
            with open(self.__path / 'data.pkl', 'wb') as file:
                pickle.dump(self.__data, file)

    def load(self) -> Data:
        path = self.__path / 'data.pkl'
        if path.exists():
            try:
                with open(path , 'rb') as file:
                    data =  pickle.load(file)
                    if isinstance(data, Data):
                        self.__data = data
                        return data
            except Exception as _: pass
        self.__data = Data()
        return self.__data 
