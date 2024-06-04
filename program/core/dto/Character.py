class Character:
    """
    사진에서의 얼굴 위치와 이름을 가지고 있음
    """
    def __init__(self, name: int, location: tuple[int]):
        self.__name: int = name
        self.__location: tuple[int] = location

    def get_name(self) -> int:
        return self.__name

    def get_location(self) -> tuple[int]:
        return self.__location