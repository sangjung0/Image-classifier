import pathlib
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QFileDialog, QHBoxLayout
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QCloseEvent

from gui.Utils import message_box


class PathModal(QWidget):
    """
    PathModal 경로 지정 모달
    """
    __WIDTH:int = 600
    __HEIGHT:int = 50
    def __init__(self, center:QPoint, confirm_callback: callable, cancel_callback:callable, confirm_name: str, cancel_name: str):
        """
        center -- QPoint 모달 center 위치
        confirm_callback -- callable 성공시 실행 함수
        cancel_callback -- callable 실패시 실행 함수
        confirm_name -- 성공 버튼 이름
        cancel_name -- 취소 버튼 이름
        """
        super().__init__()
        self.__path_input:QLineEdit = QLineEdit(self)
        self.__confirm_callback:callable = confirm_callback
        self.__cancel_callback: callable = cancel_callback
        self.__status:bool = False
        
        self.__init_ui(confirm_name, cancel_name , center)
    
    def __init_ui(self, confirm_name:str, cancel_name:str, center:QPoint):
        """
        Ui 위치 및 이벤트 지정
        """
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        
        self.__path_input.setPlaceholderText("Enter path or click 'Browse' to select")
        h_layout.addWidget(self.__path_input, 8)
        
        browse_button = QPushButton("Browse", self)
        browse_button.clicked.connect(self.__button_event)
        h_layout.addWidget(browse_button, 2)
        
        v_layout.addLayout(h_layout)
        
        h_layout = QHBoxLayout()
        
        success_button = QPushButton(confirm_name, self)
        success_button.clicked.connect(self.__set_event)
        h_layout.addWidget(success_button, 5)
        
        cancel_button = QPushButton(cancel_name, self)
        cancel_button.clicked.connect(self.close)
        h_layout.addWidget(cancel_button,5)
        
        v_layout.addLayout(h_layout)
        
        self.setLayout(v_layout)
        self.setWindowTitle("Select Path")
        
        print(center.x(), center.y())
        self.setGeometry(center.x() - PathModal.__WIDTH//2, center.y() - PathModal.__HEIGHT//2, PathModal.__WIDTH, PathModal.__HEIGHT)
        
    def closeEvent(self, event:QCloseEvent):
        if not self.__status: 
            self.__cancel_callback()
        super().closeEvent(event)
        

    def __button_event(self):
        """
        Browse 버튼 이벤트
        """
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        result = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)
        if result:
            self.__path_input.setText(result)

    def __set_event(self):
        """
        Success Button 이벤트
        """
        path = pathlib.Path(self.__path_input.text())
        if path.exists() and path.is_dir():
            self.__status = True
            self.__confirm_callback(path)
            self.close()
        else:
            self.__status = False
            message_box(self, "Invalid path", "The specified path does not exist or is not a directory. Please try again.")
        
