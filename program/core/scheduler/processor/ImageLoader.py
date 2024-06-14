import PIL.Image
import numpy as np

from core.scheduler.processor.Processor import Processor
from core.scheduler.dto import Packet
from core.Histogram import Histogram

from core.Constant import MAX_IMAGE_SIZE

class ImageLoader(Processor):
    """이미지를 읽고, 스케일 조정을 하며 히스토그램 값을 구함."""
    
    def __init__(self, name:str, loger_is_print:bool = False)->None:
        super().__init__(name, loger_is_print)
        
    def processing(self, value:Packet)->Packet:
        for i in value:
            path = i.path
            if path == None: break
            image = None
            try:
                with PIL.Image.open(path) as img:
                    img = img.convert('RGB')
                    width, height = img.size
                    if max(width, height) > MAX_IMAGE_SIZE:
                        if width > height:
                            height = int(height/width*MAX_IMAGE_SIZE)
                            i.scale = width/MAX_IMAGE_SIZE
                            width = MAX_IMAGE_SIZE
                        else:
                            width = int(width/height*MAX_IMAGE_SIZE)
                            i.scale = height/MAX_IMAGE_SIZE
                            height = MAX_IMAGE_SIZE
                    img = img.resize((width,height), PIL.Image.LANCZOS)
                    image = np.array(img, dtype=np.uint8)
                    i.histogram = Histogram.calculate_histogram(image)
                    i.image = image
            except FileNotFoundError as _:
                continue    
        
        return value