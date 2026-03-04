from gtts import gTTS, gTTSError
import pygame
from gui.gui import GUI
from time import sleep

class TTS:
    def __init__(self):

#-------переменные------------------------------------------------------------------------------------------------------

        self.answer = ""
        self.tts = None

#-------функция-озвучки-текста------------------------------------------------------------------------------------------
    def speak(self, answer: str):
        try:

#-------загружаем-озвученные-текст-в-файл-------------------------------------------------------------------------------

            self.answer = answer

            if self.answer.split()[1].find("://") != -1:
                self.tts = gTTS(text=self.answer.split()[0], lang="ru")
                self.tts.save("work_with_voice/voice/output.mp3")
            else:
                self.tts = gTTS(text=self.answer, lang="ru")
                self.tts.save("work_with_voice/voice/output.mp3")

#-------озвучка-текста--------------------------------------------------------------------------------------------------

            pygame.mixer.init()
            pygame.mixer.music.load("work_with_voice/voice/output.mp3")
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.music.unload()
            pygame.mixer.quit()

        except gTTSError:
            GUI.error(self)
            sleep(0.5)
