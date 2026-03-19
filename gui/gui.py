from PyInstaller.utils.hooks.setuptools import pre_safe_import_module_for_top_level_namespace_packages
from PyQt5 import QtWidgets as Qt
from PyQt5.QtGui import QMovie, QIcon
from PyQt5.QtWidgets import QMessageBox, QWidget, QVBoxLayout
from PyQt5 import QtCore
from functionale.ai.AI import AI
from random import choice

class AIWork(QtCore.QThread):
    AI_answer = QtCore.pyqtSignal(str)

    def __init__(self, promt):
        super().__init__()
        self.promt = promt

    def run(self):
        ai = AI()
        answer = ai.promt_and_answer(self.promt)
        self.AI_answer.emit(answer)

class GUI:
    def __init__(self):

#-------переменные------------------------------------------------------------------------------------------------------

        self.is_live = False
        self.start = False
        self.working_time = 0
        self.ai_thread = None
        self.hello_variants = ["Тут пока тихо. Напиши первым", "Никто ещё не написал… исправим", "Начни разговор — я готова"]

#-------окно------------------------------------------------------------------------------------------------------------

        self.window = Qt.QMainWindow()
        self.window.setWindowTitle('RoboSenku')
        self.window.setFixedSize(950, 520)
        self.window.closeEvent = self.close_event

#-------фон-------------------------------------------------------------------------------------------------------------

        self.background = Qt.QLabel(self.window)
        self.background.setFixedSize(950,520)
        self.background.setStyleSheet("""
        QLabel {
            background: qlineargradient(
                x1: 0, y1: 1,
                x2: 1, y2: 0,
                stop:0   #000000,
                stop:1   #1e1e1e
        );
    }
""")

#-------гиф-------------------------------------------------------------------------------------------------------------

        self.rs_gif = QMovie("./images/RoboSenkuSprites/gifs/rsGif.gif")

        self.rs_gif.start()

#-------Лейбл-Робо-Сенку------------------------------------------------------------------------------------------------

        self.rs_label = Qt.QLabel(self.window)
        self.rs_label.setGeometry(0,0,420,520)
        self.rs_label.setScaledContents(True)
        self.rs_label.setMovie(self.rs_gif)

#-------контейнер-кнопки-начала-----------------------------------------------------------------------------------------

        self.start_button_container = Qt.QLabel(self.window)
        self.start_button_container.setGeometry(0,300,420,220)
        self.start_button_container.setStyleSheet("""
        border-top-left-radius: 30px;
        border-top-right-radius: 30px;
        background: qlineargradient(
            x1:0, y1:1,
            x2:1, y2:0,
            stop:0    #141414,
            stop:1    #1e1e1e
        );
        border: 2px solid #303030        
        """)

#-------контейнер-чата--------------------------------------------------------------------------------------------------

        self.chat_container = Qt.QLabel(self.window)
        self.chat_container.setGeometry(440,20,495,485)
        self.chat_container.setStyleSheet("""
        border-radius: 30px;
        background: qlineargradient(
            x1:1, y1:0,
            x2:1, y2:0,
            stop:0   #1f1f1f,
            stop:1   #2a2a2a
        );          
        border: 2px solid #303030
        """)

#-------вывеска-пока-нету-сообщений-чате--------------------------------------------------------------------------------

        self.hello_title = Qt.QLabel(self.chat_container)
        self.hello_title.setFixedSize(495, 300)
        self.hello_title.setWordWrap(True)
        self.hello_title.setText(choice(self.hello_variants))
        self.hello_title.setAlignment(QtCore.Qt.AlignCenter)
        self.hello_title.setStyleSheet("""
        background-color:transparent; 
        border: 0px;
        font-size: 40px;
        padding: 10px;
        color: #cfcfcf 
    """)

#-------место-ввода-----------------------------------------------------------------------------------------------------

        self.input_place = Qt.QLineEdit(self.chat_container)
        self.input_place.setGeometry(15,400,405,60)
        self.input_place.setStyleSheet("""
        QLineEdit{
        border-radius: 30px;
        background: qlineargradient(
            x1:0, y1:0,
            x2:0, y2:1,
            stop:0   #161616,   
            stop:1   #262626  
        );
        font-size: 20px;
        caret-color: #BDBDBD;
        color: #BDBDBD;
        }
        QLineEdit:focus{
        border: 2px solid #888888 ;
        }
        """)
        self.input_place.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.input_place.setPlaceholderText("  Сообщение...")
        self.input_place.returnPressed.connect(self.sending)


#-------кнопка-отправки-текста------------------------------------------------------------------------------------------

        self.enter_button = Qt.QPushButton(self.chat_container)
        self.enter_button.setGeometry(465-35,405,50,50)
        self.enter_button.setStyleSheet("""
        QPushButton{
            background-color: #e8e8e8;
            border-radius: 25px;
            border: 2px solid #fcfcfc;
        }
        QPushButton:hover{
            background-color: #f6f6f6;
            border: 2px solid #fcfcfc;
        }
        QPushButton:pressed{
            background-color: #fff;
        }
        """)
        self.enter_button.setIcon(QIcon("./images/icons/send.svg"))
        self.enter_button.setIconSize(QtCore.QSize(28,28))
        self.enter_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.enter_button.clicked.connect(self.sending)

#------скролер----------------------------------------------------------------------------------------------------------

        self.chat_scroller = Qt.QScrollArea(self.window)
        self.chat_scroller.setGeometry(465,30,455,380) #495,485

        self.chat_scroller.setStyleSheet("""
        QScrollArea{
            border: none;
            background: transparent;
        }

        QScrollBar:vertical{
            background: #1e1e1e;
            width: 10px;
            margin: 0px;
            border-radius: 5px;
        }

        QScrollBar::handle:vertical{
            background: #fcfcfc;
            min-height: 30px;
            border-radius: 5px;
        }


        QScrollBar::handle:vertical:hover{
            background: #fff;
        }


        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical{
            height: 0px;
        }

        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical{
            background: none;
        }
        """)
        self.chat_scroller.verticalScrollBar().setCursor(QtCore.Qt.PointingHandCursor)
        self.chat_scroller.setWidgetResizable(True)

        # ---контент---

        self.scroller_content = QWidget()
        self.scroller_content.setStyleSheet("background-color: transparent")

        # ---лаяют---

        self.scroller_layout = QVBoxLayout(self.scroller_content)
        self.scroller_layout.setSpacing(25)

        self.scroller_layout.setAlignment(QtCore.Qt.AlignTop)


        self.chat_scroller.setWidget(self.scroller_content)




#-------кнопка-начала-программы-----------------------------------------------------------------------------------------

        self.start_button = Qt.QPushButton(self.start_button_container)
        self.start_button.setGeometry(25,100,370,100)
        self.start_button.setText("начать")
        self.start_button.setStyleSheet("""
        QPushButton{
            background: transparent;
            border-radius: 20px;
            border: 2px solid #BDBDBD ;
            color: #BDBDBD ;
            font-size:20px
        }
        
        QPushButton:hover{
            border: 3px solid #FFFAF0 ;
            color: #FFFAF0 ;
            font-size:20px
        }
        
        QPushButton:pressed{
            border: 2px solid #fff ;
            color: #fff ;
        }
        """)
        self.start_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.start_button.clicked.connect(self.start_program)

#-------таймер----------------------------------------------------------------------------------------------------------

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.start_time)

#-------загружаем-короче-апи-что-бы-пользователь-не-ждал----------------------------------------------------------------

        self.ai_thread =  AIWork(" ")
        self.ai_thread.AI_answer.connect(lambda _: None)
        self.ai_thread.start()


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

    def start_program(self):
        if not self.start:
            self.start_button.setStyleSheet("""
                    QPushButton{
                        background: transparent;
                        border-radius: 20px;
                        border: 2px solid #50C878 ;
                        color: #50C878 ;
                        font-size:20px
                    }
    
                    QPushButton:hover{
                        border: 3px solid #50C878;
                        color: #50C878;
                        font-size:20px
                    }
    
                    QPushButton:pressed{
                        border: 2px solid #50C878;
                        color: #50C878;
                    }
                    """)
            self.start_button.setText("00:00:00")
            self.start = not self.start
            self.is_live = not self.is_live

        else:
            self.start_button.setStyleSheet("""
                    QPushButton{
                        background: transparent;
                        border-radius: 20px;
                        border: 2px solid #BDBDBD ;
                        color: #BDBDBD ;
                        font-size:20px
                    }

                    QPushButton:hover{
                        border: 3px solid #FFFAF0 ;
                        color: #FFFAF0 ;
                        font-size:20px
                    }

                    QPushButton:pressed{
                        border: 2px solid #fff ;
                        color: #fff ;
                    }
                    """)
            self.start_button.setText("начать")
            self.start = not self.start
            self.is_live = not self.is_live

        if self.start:
            self.timer.start(1000)
        else:
            self.timer.stop()
            self.working_time = 0

    def start_time(self):
        hours = self.working_time // 3600
        minutes = (self.working_time % 3600) // 60
        secs = self.working_time % 60
        self.working_time += 1
        self.start_button.setText(f"{hours:02}:{minutes:02}:{secs:02}")

    def sending(self):
        if self.input_place.text().strip() != "":

            self.hello_title.hide()

            user_label = Qt.QLabel(self.input_place.text())
            user_label.setWordWrap(True)
            user_label.setMaximumWidth(300)
            user_label.setStyleSheet("""
                    background-color: #4a4a4a;
                    color: #fcfcfc;
                    font-size: 20px;
                    border-radius: 15px;
                    padding: 10px;
                """)


            user_label.setFixedHeight(user_label.sizeHint().height())
            self.scroller_layout.addWidget(user_label, alignment=QtCore.Qt.AlignRight)


            self.ai_thread = AIWork(self.input_place.text())
            self.ai_thread.AI_answer.connect(self.add_ai_label)
            self.ai_thread.start()

        self.input_place.clear()


    def add_ai_label(self, answer_text):
        ai_label = Qt.QLabel(answer_text)
        ai_label.setWordWrap(True)
        ai_label.setMaximumWidth(300)
        ai_label.setStyleSheet("""
                background-color: #3b3b3b;
                color: #fcfcfc;
                font-size: 20px;
                border-radius: 15px;
                padding: 10px;
            """)

        ai_label.setFixedHeight(ai_label.sizeHint().height())
        self.scroller_layout.addWidget(ai_label, alignment=QtCore.Qt.AlignLeft)








