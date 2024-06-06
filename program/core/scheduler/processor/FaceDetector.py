import dlib
import numpy as np
from PIL import Image

from core.scheduler.processor.Processor import Processor
from core.scheduler.dto import Packet
from core.dto import Face, Character

class FaceDetector(Processor):
    def __init__(self, name:str, loger_is_print:bool = False):
        super().__init__(name, loger_is_print)
        
        self.__detector = None
        self.__sp = None
        self.__facerec = None
        
    def prepare(self):
        self.__detector = dlib.get_frontal_face_detector()
        self.__sp = dlib.shape_predictor('./program/resource/dlib-models-master/shape_predictor_68_face_landmarks.dat')
        self.__facerec = dlib.face_recognition_model_v1('./program/resource/dlib-models-master/dlib_face_recognition_resnet_model_v1.dat')
        
    def processing(self, value:Packet):
        
        for p in value:
            img = p.get_image()
            p.set_image(None)
            if img is None: continue
            dets = self.__detector(np.array(Image.fromarray(img).convert('L'), dtype=np.uint8), 1)
            if len(dets) == 0: continue
            
            for i, d in enumerate(dets):
                p.add_face(
                    i, 
                    Face(-1, np.array(self.__facerec.compute_face_descriptor(img, self.__sp(img, d))))
                )
                x = d.left()
                y = d.top()
                width = d.right() - x
                height = y - d.bottom()
                p.add_character(i, Character(-1, (x, y, width, height)))
                
        return value