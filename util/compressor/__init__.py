"""
압축 패키지
"""


from util.compressor.CompressorInterface import CompressorInterface
from util.compressor.GZipCompressor import GZipCompressor
from util.compressor.UnCompressor import UnCompressor

__all__ = ['CompressorInterface', 'GZipCompressor', 'UnCompressor']
__version__ = '0.1'