import sys
from PyQt5.QtWidgets import QApplication
from gui.gui import GUI
from work_with_voice.STT import STT
from work_with_voice.TTS import TTS
import threading
from functionale.ai.AI import AI
from functionale.base.base import Copy, Link, Close
from time import sleep


#-------функция-связывания-логики---------------------------------------------------------------------------------------

def voice(gui):
    while True:
        try:
            while gui.is_live:
                ai = AI()
                stt = STT()
                tts = TTS()

                answer = ai.promt_and_answer(stt.text)
                if stt.text != "":
                    Copy(answer, stt.text)
                    Link(answer, stt.text)
                    Close(stt.text)
                    tts.speak(answer)

        except AttributeError:
            gui.error()
            sleep(1)

        except OSError:
            gui.error()
            sleep(1)

#-------точка-входа-----------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GUI()
    window.show()

    t = threading.Thread(target=voice, args=(window,), daemon=True)
    t.start()

    sys.exit(app.exec_())
