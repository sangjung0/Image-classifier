from PyQt5.QtWidgets import QMessageBox, QWidget

def message_box(parent:QWidget, title:str, message:str, b_type = QMessageBox.Warning):
        alert = QMessageBox(parent)
        alert.setWindowTitle(title)
        alert.setText(message)
        alert.setIcon(b_type)
        alert.addButton(QMessageBox.Ok)
        alert.exec_()