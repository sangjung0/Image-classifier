import pathlib
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QFileDialog, QHBoxLayout, QDialog
from PyQt5.QtCore import QPoint

from gui.Utils import message_box
from gui.Constant import PATH_MODAL_HEIGHT, PATH_MODAL_WIDTH


class PathModal(QDialog):
    """
    PathModal 경로 지정 모달
    """
    def __init__(self, base:QWidget, callback:callable, confirm_name: str, cancel_name: str) -> None:
        """
        callback -- callable 성공시 실행 함수
        confirm_name -- 성공 버튼 이름
        cancel_name -- 취소 버튼 이름
        """
        super().__init__(base)
        self.__path_input:QLineEdit = QLineEdit(self)
        self.__callback:callable = callback
                
        self.setModal(True)
        self.__init_ui(confirm_name, cancel_name)
        
    def show(self, center:QPoint) -> None:
        """
        center -- QPoint 모달 center 위치
        """
        self.setGeometry(center.x() - PATH_MODAL_WIDTH//2, center.y() - PATH_MODAL_HEIGHT//2, PATH_MODAL_WIDTH, PATH_MODAL_HEIGHT)
        super().show()
    
    def __init_ui(self, confirm_name:str, cancel_name:str) -> None:
        """
        Ui 위치 및 이벤트 지정
        """
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        
        self.__path_input.setPlaceholderText("Enter path or click 'Browse' to select")
        h_layout.addWidget(self.__path_input, 8)
        
        browse_button = QPushButton("Browse", self)
        browse_button.clicked.connect(self.__browse_event)
        h_layout.addWidget(browse_button, 2)
        
        v_layout.addLayout(h_layout)
        
        h_layout = QHBoxLayout()
        
        success_button = QPushButton(confirm_name, self)
        success_button.clicked.connect(self.__confirm_event)
        h_layout.addWidget(success_button, 5)
        
        cancel_button = QPushButton(cancel_name, self)
        cancel_button.clicked.connect(self.close)
        h_layout.addWidget(cancel_button,5)
        
        v_layout.addLayout(h_layout)
        
        self.setLayout(v_layout)
        self.setWindowTitle("Select Path")
        
    def __browse_event(self) -> None:
        """
        Browse 버튼 이벤트
        """
        result = QFileDialog.getExistingDirectory(self, "Select Folder", options=QFileDialog.Options())
        if result:
            self.__path_input.setText(result)

    def __confirm_event(self) -> None:
        """
        Success Button 이벤트
        """
        path = pathlib.Path(self.__path_input.text())
        if path.exists() and path.is_dir():
            self.__callback(path)
            self.close()
        else:
            message_box(self, "Invalid path", "The specified path does not exist or is not a directory. Please try again.")
        
