"""
얼굴 탐지 알고리즘
"""

from face_detector.MyMTCNN import MyMTCNN
from face_detector.HaarCascade import HaarCascade
from face_detector.FaceDetectorFilter import FaceDetectorFilter

__all__ = ['MyMTCNN', 'HaarCascade', 'FaceDetectorFilter']
__version__ = '0.1'