import speech_recognition as sr
from gui.gui import GUI
from time import sleep

class STT:
    def __init__(self):
        try:

#-------рекогнайзер-----------------------------------------------------------------------------------------------------

            self.rec = sr.Recognizer()

#-------слушаем-микрофон------------------------------------------------------------------------------------------------

            with sr.Microphone() as s:
                self.rec.adjust_for_ambient_noise(s)
                self.audio = self.rec.listen(s)

#-------распознаем-текст------------------------------------------------------------------------------------------------

            try:
                self.text = self.rec.recognize_google(self.audio, language="ru-RU")
                print(self.text)
#-------если-текст-не-распознан------------------------------------------------------------------------------------------

            except sr.UnknownValueError:
                self.text = ""

        except sr.exceptions.RequestError:
            GUI.error(self)
            sleep(0.5)
