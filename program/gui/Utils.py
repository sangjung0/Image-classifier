from PyQt5.QtWidgets import QMessageBox, QWidget

def message_box(parent:QWidget, title:str, message:str):
        alert = QMessageBox(parent)
        alert.setWindowTitle(title)
        alert.setText(message)
        alert.setIcon(QMessageBox.Warning)
        alert.addButton(QMessageBox.Ok)
        alert.exec_()