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
