from datetime import datetime
import timeit

class AllProcessIsTerminated:
    def __init__(self, processes):
        self.__processes = processes

    def allProcessIsTerminated(self):
        return not any(p.is_alive() for p in self.__processes)
    
    def wait(self):
        for p in self.__processes:
            p.join(1)
            if p.is_alive(): p.terminate()

class AllTransmissionMediumIsTerminated:
    def __init__(self, mediums):
        self.__mediums = mediums
    
    def wait(self):
        for m in self.__mediums:
            m.close()
            m.join_thread()

class Timer:
    def __init__(self):
        self.__startTime = None
        self.__endTime = None
        self.__duration = None

    @property
    def startTime(self):
        return self.__startTime

    @property
    def endTime(self):
        return self.__endTime
    
    @property
    def duration(self):
        return self.__duration

    def start(self):
        self.__startTime = timeit.default_timer()
        self.__endTime = None
        self.__duration = None
    
    def end(self):
        if self.__startTime is None: raise Exception("타이머 시작 안함")
        self.__endTime = timeit.default_timer()
        self.__duration = self.__endTime - self.__startTime

    def __str__(self):
        return f"Time: {round(self.duration, 5)}s"
    
class Loger:
    def __init__(self, name, isPrint = True):
        self.__name = name
        self.__isPrint = isPrint

    def __call__(self,*msg, timer:Timer = None):
        if self.__isPrint:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] - {self.__name.ljust(20)} - {str(timer if timer else None).ljust(20)}: ", " ".join(str(i) for i in msg))
