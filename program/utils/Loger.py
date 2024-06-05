from datetime import datetime

class Loger:
    def __init__(self, name, isPrint = True):
        self.__name = name
        self.__isPrint = isPrint

    def __call__(self,*msg, option:object = None):
        if self.__isPrint:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] - {self.__name.ljust(30)} - {str(option if option else None).ljust(20)}: ", " ".join(str(i) for i in msg))