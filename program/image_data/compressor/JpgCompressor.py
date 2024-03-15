import numpy as np
from PIL import Image
import io

from process.compressor.CompressorInterface import CompressorInterface

class JpgCompressor(CompressorInterface):
    
    def compress(self, value:np.ndarray):
        byteIo = io.BytesIO()
        Image.fromarray(value).save(byteIo, format='JPEG')
        return byteIo.getvalue()
    
    def decompress(self, value: bytes) -> np.ndarray:
        return np.array(Image.open(io.BytesIO(value)))
