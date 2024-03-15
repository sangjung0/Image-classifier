"""
얼굴 탐지 알고리즘
"""

from process.face_detector.DetectorInterface import DetectorInterface

from process.face_detector.HaarCascade import HaarCascade
from process.face_detector.MyMTCNN import MyMTCNN

__all__ = ['MyMTCNN', 'HaarCascade', 'DetectorInterface']
__version__ = '0.1'