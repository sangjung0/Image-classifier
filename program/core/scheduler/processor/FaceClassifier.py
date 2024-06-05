from core.scheduler.processor.Processor import Processor

from core.scheduler.dto import Packet

class FaceClassifier(Processor):
    def __init__(self, name:str, loger_is_print:bool = False):
        super().__init__(name, loger_is_print)
    
    def processing(self, value:Packet):
        
        
        return value