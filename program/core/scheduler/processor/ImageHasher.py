import PIL.Image
import numpy as np

from core.scheduler.processor.Processor import Processor
from core.scheduler.dto import Packet
from core.Histogram import Histogram

class ImageHasher(Processor):
    
    __MAX_SIZE:int = 720
    
    def __init__(self, name:str, loger_is_print:bool = False):
        super().__init__(name, loger_is_print)
        
    def prepare(self): pass
            
    def processing(self, value:Packet):
        for i in value:
            path = i.path
            if path == None: break
            image = None
            try:
                with PIL.Image.open(path) as img:
                    img = img.convert('RGB')
                    width, height = img.size
                    if max(width, height) > ImageHasher.__MAX_SIZE:
                        if width > height:
                            height = int(height/width*ImageHasher.__MAX_SIZE)
                            i.scale = width/ImageHasher.__MAX_SIZE
                            width = ImageHasher.__MAX_SIZE
                        else:
                            width = int(width/height*ImageHasher.__MAX_SIZE)
                            i.scale = height/ImageHasher.__MAX_SIZE
                            height = ImageHasher.__MAX_SIZE
                    img = img.resize((width,height), PIL.Image.LANCZOS)
                    image = np.array(img, dtype=np.uint8)
                    i.histogram = Histogram.calculate_histogram(image)
                    i.image = image
            except Exception as _:
                continue    
        
        return value