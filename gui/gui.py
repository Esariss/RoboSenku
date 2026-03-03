from PyQt5 import QtWidgets as Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QMessageBox

class GUI:
    def __init__(self):

#-------переменные------------------------------------------------------------------------------------------------------

        self.is_live = True

#-------окно------------------------------------------------------------------------------------------------------------

        self.window = Qt.QMainWindow()
        self.window.setWindowTitle('RoboSenku')
        self.window.setFixedSize(420, 520)
        self.window.closeEvent = self.close_event

#-------фон-------------------------------------------------------------------------------------------------------------

        self.background = Qt.QLabel(self.window)
        self.background.setFixedSize(420,520)
        self.background.setStyleSheet("""
        QLabel {
            background: qradialgradient(
                cx:0.5, cy:0.5,
                radius:0.5,
                fx:0.5, fy:0.5,
                stop:0   #000000,
                stop:0.1 #030303,
                stop:0.2 #060606,
                stop:0.3 #090909,
                stop:0.4 #0c0c0c,
                stop:0.5 #0f0f0f,
                stop:0.6 #121212,
                stop:0.7 #151515,
                stop:0.8 #181818,
                stop:0.9 #1b1b1b,
                stop:1   #1e1e1e
        );
    }
""")

#-------гиф-------------------------------------------------------------------------------------------------------------

        self.rs_gif = QMovie("./images/RoboSenkuSprites/gifs/rsGif.gif")

        self.rs_gif.start()

#-------Лейбл-Робо-Сенку------------------------------------------------------------------------------------------------

        self.rs_label = Qt.QLabel(self.window)
        self.rs_label.setFixedSize(420,520)
        self.rs_label.setScaledContents(True)
        self.rs_label.setMovie(self.rs_gif)

#-------кнопка начала программы------------------------------------------------------------------------------------------------

    def show(self):
        self.window.show()

    def close_event(self, event):
        self.is_live = False
        event.accept()

    def error(self):
        QMessageBox.critical(
            self.window,
            "Error",
            "проверьте наличие микрофона и интернета"
        )


