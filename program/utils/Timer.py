import timeit

class Timer:
    def __init__(self, round = 5):
        self.__startTime = None
        self.__endTime = None
        self.__duration = None
        self.__avg = None
        self.__round = round

    @property
    def startTime(self):
        return round(self.__startTime, self.__round)

    @property
    def endTime(self):
        return round(self.__endTime, self.__round)
    
    @property
    def duration(self):
        return round(self.__duration, self.__round)
    
    @property    
    def average(self):
        if self.__avg is None: return 0
        return round(self.__avg, self.__round)
    
    def measure(self, func:callable):
        self.start()
        result = func()
        self.end()
        return result

    def start(self):
        self.__startTime = timeit.default_timer()
        self.__endTime = None
        self.__duration = None
    
    def end(self):
        if self.__startTime is None: raise Exception("타이머 시작 안함")
        self.__endTime = timeit.default_timer()
        self.__duration = self.__endTime - self.__startTime
        self.__avg = self.__duration if self.__avg is None else (self.__avg + self.__duration) / 2


    def __str__(self):
        return f"Time: {self.duration}s"