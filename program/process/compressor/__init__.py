"""
압축 패키지
"""


from process.compressor.CompressorInterface import CompressorInterface
from process.compressor.GZipCompressor import GZipCompressor
from process.compressor.UnCompressor import UnCompressor
from process.compressor.JpgCompressor import JpgCompressor

__all__ = ['CompressorInterface', 'GZipCompressor', 'UnCompressor', 'JpgCompressor']
__version__ = '0.1'