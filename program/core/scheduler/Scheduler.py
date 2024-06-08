import pathlib
from collections import deque
from multiprocessing import Process, Queue, Value
from multiprocessing.sharedctypes import SynchronizedBase
from threading import Thread, Lock
import time
import queue as EQ
import gc

from core.dto import Data
from core.scheduler.dto import Converter, Packet, PacketData
from core.scheduler.processor import *
from core.scheduler.transceiver import *
from core.Constant import PROCESSOR_STOP, PROCESSOR_PAUSE, PROCESSOR_START

from utils import Loger, Timer

class Scheduler:
    """
    이미지 분석을 수월하게 하기 위한 멀티 프로세싱 스케줄 클래스
    """
    def __init__(self, data:Data, paths:list[pathlib.Path]) -> None:
        """
        Args:
            data (Data): 이미지 정보를 참조 함
            paths (list[pathlib.Path]): 분석할 이미지 경로 
        """
        
        self.__queue: deque[pathlib.Path] = deque(paths)
        self.__name:str = "scheduler"
        self.__loger_is_print:bool = False
        self.__data:Data = data
        self.__lock:Lock = Lock()
        self.__processes:list[Process] = []
        self.__threads:list[Thread] = []
        self.__queues:list[Queue] = []
        self.__flag:SynchronizedBase = None

    def add(self, path: pathlib.Path) -> None:
        with self.__lock:
            self.__queue.appendleft(path)
            
    def poll(self) -> pathlib.Path:
        with self.__lock:
            return self.__queue.popleft()

    def is_empty(self) -> bool:
        return len(self.__queue) == 0

    def run(self, buf_size:int, packet_size:int) ->None:
        """멀티 프로세싱 시작 점. 이미지 해시 값, 얼굴 탐지, 얼굴 인식을 진행

        Args:
            buf_size (int): 멀티프록세싱 큐 사이즈
            packet_size (int): 패킷 사이즈
        """

        
        self.__flag:SynchronizedBase = Value('i',PROCESSOR_PAUSE)
        termination_signal:SynchronizedBase = Value('i', 0)
        termination_order = 0
        
        output_sch_input_ih_queue = Queue(maxsize=buf_size)
        output_ih_input_fd_queue = Queue(maxsize=buf_size)
        output_fd_input_fc_queue = Queue(maxsize=buf_size)
        output_fr_input_sch_queue = Queue(maxsize=buf_size)
        
        termination_order += 1
        image_hasher_1 = Process(
            target=ImageLoader("imageHasher_1", self.__loger_is_print),
            args=(termination_order, termination_signal, self.__flag, output_sch_input_ih_queue, output_ih_input_fd_queue)
        )                      
        termination_order += 1
        image_hasher_2 = Process(
            target=ImageLoader("imageHasher_2", self.__loger_is_print),
            args=(termination_order, termination_signal, self.__flag, output_sch_input_ih_queue, output_ih_input_fd_queue)
        )                      
        termination_order += 1
        image_hasher_3 = Process(
            target=ImageLoader("imageHasher_3", self.__loger_is_print),
            args=(termination_order, termination_signal, self.__flag, output_sch_input_ih_queue, output_ih_input_fd_queue)
        )                   
        termination_order += 1
        face_detector_1 = Process(
            target = FaceDetector("faceDetector_1", self.__loger_is_print),
            args = (termination_order, termination_signal, self.__flag, output_ih_input_fd_queue, output_fd_input_fc_queue)
        )
        termination_order += 1
        face_detector_2 = Process(
            target = FaceDetector("faceDetector_2", self.__loger_is_print),
            args = (termination_order, termination_signal, self.__flag, output_ih_input_fd_queue, output_fd_input_fc_queue)
        )
        termination_order += 1
        face_detector_3 = Process(
            target = FaceDetector("faceDetector_3", self.__loger_is_print),
            args = (termination_order, termination_signal, self.__flag, output_ih_input_fd_queue, output_fd_input_fc_queue)
        )
        termination_order += 1
        face_classifier = Process(
            target = FaceClassifier("faceClassifier", self.__data.faces, self.__loger_is_print),
            args = (termination_order, termination_signal, self.__flag, output_fd_input_fc_queue, output_fr_input_sch_queue)
        )
        
        image_hasher_1.start()
        image_hasher_2.start()
        image_hasher_3.start()
        face_detector_1.start()
        face_detector_2.start()
        face_detector_3.start()
        face_classifier.start()
        
        termination_order += 1
        sender = Thread(target=self.__sender, args=(packet_size, termination_signal, output_sch_input_ih_queue))
        receiver = Thread(target=self.__receiver, args=(termination_order, termination_signal, output_fr_input_sch_queue))
        sender.start()
        receiver.start()
        
        self.__queues.append(output_sch_input_ih_queue)
        self.__queues.append(output_ih_input_fd_queue)
        self.__queues.append(output_fd_input_fc_queue)
        self.__queues.append(output_fr_input_sch_queue)
        
        self.__processes.append(image_hasher_1)
        self.__processes.append(image_hasher_2)
        self.__processes.append(image_hasher_3)
        self.__processes.append(face_detector_1)
        self.__processes.append(face_detector_2)
        self.__processes.append(face_detector_3)
        self.__processes.append(face_classifier)
        
        self.__threads.append(sender)
        self.__threads.append(receiver)
        
        self.__flag.value = PROCESSOR_START
        
    def close(self) -> None:
        if self.__flag is None: return
        
        self.__flag.value = PROCESSOR_STOP
        
        for p in self.__processes: p.join(0.1)
        for q in self.__queues:
            q.close()
            q.join_thread()
        for t in self.__threads:
            t.join(0.1)
        
    def __sender(self, packet_size:int, termination_signal: SynchronizedBase, queue:Queue) -> None:
        # --
        loger = Loger(self.__name + "Sender", self.__loger_is_print) # logger
        timer = Timer() # timer
        loger("start") # loge
        # --
        converter = Converter(queue)
        packet = Packet([PacketData(None) for _ in range(packet_size)])
        packet_ary = packet.data
        i = 0
        try:
            while True:
                if self.is_empty():
                    if i == 0: break
                    for i in range(packet_size): packet_ary[i].path = None
                    timer.measure(lambda: converter.send(packet))
                    break
                if self.__flag.value == PROCESSOR_PAUSE:
                    time.sleep(0.1)
                elif self.__flag.value == PROCESSOR_STOP:
                    break
                else:
                    path = self.poll()
                    image = self.__data.get_image(path)
                    if image.is_scheduled: continue
                    image.is_scheduled = True
                    packet_ary[i].path = path
                    i += 1
                    if i == packet_size:
                        i = 0
                        timer.measure(lambda: converter.send(packet))
                        loger("데이터 압축 후 송신", option=timer)
        except Exception as e:
            loger("쓰레드 오류",e, option="error") # loger
            self.__flag.value = PROCESSOR_STOP
        loger(f"데이서 송신 평균 속도 {timer.average}", option='result') # loger
        loger("쓰레드 종료", option='terminate') # loger
        termination_signal.value += 1
        
        
    def __receiver(self, order: int, termination_signal: SynchronizedBase, queue:Queue) -> None:
        # --
        loger = Loger(self.__name+"Receiver", self.__loger_is_print) # logger
        timer = Timer() # timer
        loger("start") # loge
        # --
        converter = Converter(queue)
        
        try:
            while True:
                if self.__flag.value == PROCESSOR_PAUSE:
                    time.sleep(0.1)
                elif self.__flag.value == PROCESSOR_STOP:
                    break
                else:
                    try:
                        ret, data = timer.measure(lambda : converter.receive())
                        loger("데이터 수신 후 압축 해제", option=timer)
                        if ret: 
                            for i in data:
                                if i.path == None: break
                                image = self.__data.get_image(i.path)
                                characters = i.characters
                                for k in characters:
                                    image.characters[k] = characters[k]
                                faces = i.faces
                                for k in faces:
                                    self.__data.set_face(k, faces[k])
                                image.histogram = i.histogram
                                image.is_detected = True
                    except EQ.Empty:
                        if termination_signal.value >= order:
                            break
                    gc.collect()
        except Exception as e:
            loger("쓰레드 오류",e, option="error") # loger
            self.__flag.value = PROCESSOR_STOP
        loger(f"데이서 수신 후 압축 해제 평균 속도 {timer.average}", option='result') # loger
        loger("쓰레드 종료", option='terminate') # loger
        