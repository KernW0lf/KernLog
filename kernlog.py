#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QTimer
import subprocess
import pyfiglet

class LiveDmesgViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Live dmesg Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.banner_label = QLabel(self.central_widget)
        self.layout.addWidget(self.banner_label)

        self.txt_log = QTextEdit(self.central_widget)
        self.txt_log.setReadOnly(True)
        self.layout.addWidget(self.txt_log)

        self.btn_clear = QPushButton("Clear Log", self.central_widget)
        self.btn_clear.clicked.connect(self.clear_log)
        self.layout.addWidget(self.btn_clear)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.read_dmesg)
        self.timer.start(500)  

        self.read_dmesg()  

        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
                color: #333;
                font-family: Arial, sans-serif;
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 5px 10px;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

        self.set_banner()

    def set_banner(self):
        banner_text = pyfiglet.figlet_format("KernW0lf", font="digital")
        self.banner_label.setText(banner_text)
        self.banner_label.setStyleSheet("color: #007bff; font-size: 24px;")

    def read_dmesg(self):
        try:
            result = subprocess.run(['dmesg', '-H', '-k'], stdout=subprocess.PIPE, text=True)
            output = result.stdout
            self.txt_log.clear()
            self.txt_log.insertPlainText(output)
            self.txt_log.verticalScrollBar().setValue(self.txt_log.verticalScrollBar().maximum())
        except Exception as e:
            self.txt_log.insertPlainText(f"Error running dmesg: {str(e)}\n")

    def clear_log(self):
        try:
            subprocess.run(['dmesg', '-C'])
            self.txt_log.clear()
        except Exception as e:
            self.txt_log.insertPlainText(f"Error clearing log: {str(e)}\n")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = LiveDmesgViewer()
    viewer.show()
    sys.exit(app.exec_())
