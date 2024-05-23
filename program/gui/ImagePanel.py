import pathlib
import numpy as np


class ImagePanel:
    __DEFAULT_IMAGE: pathlib.Path = ""

    def __init__(self):
        pass

    def set_image(self, image: np.ndarray):
        pass

    def resize_image(self, scale: float):
        pass

    def __set_default_image(self):
        pass
