class AllProcessIsTerminated:
    def __init__(self, processes):
        self.__processes = processes

    def allProcessIsTerminated(self):
        return not any(p.is_alive() for p in self.__processes)