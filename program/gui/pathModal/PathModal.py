import pathlib
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QFileDialog, QHBoxLayout
from PyQt5.QtCore import QPoint

from gui.Utils import message_box


class PathModal(QWidget):
    """
    PathModal 경로 지정 모달
    """
    __WIDTH:int = 600
    __HEIGHT:int = 50
    def __init__(self, center:QPoint, success_callback: callable, cacel_callback:callable, success_name: str):
        super().__init__()
        self.__path_input:QLineEdit = QLineEdit(self)
        self.__success_callback:callable = success_callback
        self.__cacel_callback: callable = cacel_callback
        
        self.__init_ui(success_name, center)
    
    def __init_ui(self, success_name:str, center:QPoint):
        """
        Ui 위치 및 이벤트 지정
        """
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        
        self.__path_input.setPlaceholderText("Enter path or click 'Browse' to select")
        self.__path_input.textChanged.connect(self.__text_line_event)
        h_layout.addWidget(self.__path_input, 8)
        
        browse_button = QPushButton("Browse", self)
        browse_button.clicked.connect(self.__button_event)
        h_layout.addWidget(browse_button, 2)
        
        v_layout.addLayout(h_layout)
        
        h_layout = QHBoxLayout()
        
        success_button = QPushButton(success_name, self)
        success_button.clicked.connect(self.__set_event)
        h_layout.addWidget(success_button, 5)
        
        cancel_button = QPushButton("Exit", self)
        cancel_button.clicked.connect(self.__exit)
        h_layout.addWidget(cancel_button,5)
        
        v_layout.addLayout(h_layout)
        
        self.setLayout(v_layout)
        self.setWindowTitle("Select Path")
        
        self.setGeometry(center.x() - PathModal.__WIDTH//2, center.y() - PathModal.__HEIGHT//2, PathModal.__WIDTH, PathModal.__HEIGHT)
        
    def __exit(self):
        self.close()
        self.__cacel_callback()

    def __button_event(self):
        """
        Browse 버튼 이벤트
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        result = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)
        if result:
            self.__path_input.setText(result)

    def __set_event(self):
        """
        Success Button 이벤트
        """
        path = pathlib.Path(self.__path_input.text())
        if path.exists() and path.is_dir():
            self.__success_callback(path)
            self.close()
        else:
            message_box(self, "Invalid path", "The specified path does not exist or is not a directory. Please try again.")
        
