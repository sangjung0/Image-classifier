"""
얼굴 탐지 알고리즘
"""

from image_data.face_detector.DetectorInterface import DetectorInterface

from image_data.face_detector.HaarCascade import HaarCascade
from image_data.face_detector.MyMTCNN import MyMTCNN

__all__ = ['MyMTCNN', 'HaarCascade', 'DetectorInterface']
__version__ = '0.1'