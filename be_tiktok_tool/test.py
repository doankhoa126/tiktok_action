import sys
from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from regAcc import TikTokWorker

class TiktokBotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.thread = None
        self.worker = None

    def initUI(self):
        self.layout = QVBoxLayout()
        self.startBtn_RegAcc = QPushButton('Start TikTok Bot')
        self.statusLabel = QLabel('Status: Ready')

        self.startBtn_RegAcc.clicked.connect(self.runRegAcc)

        self.layout.addWidget(self.startBtn_RegAcc)
        self.layout.addWidget(self.statusLabel)
        self.setLayout(self.layout)
        self.setWindowTitle('TikTok Bot')
        self.show()

    def runRegAcc(self):
        self.thread = QThread()
        self.worker = TikTokWorker()

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)

        self.thread.start()
        self.startBtn_RegAcc.setEnabled(False)
        self.thread.finished.connect(lambda: self.startBtn_RegAcc.setEnabled(True))

    def reportProgress(self, message):
        self.statusLabel.setText(f"Status: {message}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    botApp = TiktokBotApp()
    sys.exit(app.exec())
