"""
압축 패키지
"""


from image_data.compressor.Interface import Interface
from image_data.compressor.GZip import GZip
from image_data.compressor.UnCompressor import UnCompressor
from image_data.compressor.Jpg import Jpg

__all__ = ['Interface', 'GZip', 'UnCompressor', 'Jpg']
__version__ = '0.1'