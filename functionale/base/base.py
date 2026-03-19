import pyperclip
import webbrowser as wb
import os

class Copy:
    def __init__(self, answer: str, promt:str):
        self.answer = answer
        self.variants = [
                        "напиши",
                        "пишите",
                        "записывай",
                        "сообщи",
                        "изложи",
                        "введи",
                        "оформи",
                        "задокументируй",
                        "напиши мне",
                        "строчи",
                        "закидай текст",
                        "кинь сообщение",
                        "дропни"
                        ]
        self.promt = promt

        for i in self.variants:
            if self.promt.lower().find(i) != -1:
                pyperclip.copy(answer)

class Link:
    def __init__(self, link: str, promt: str):
        self.link = link
        self.variants = [
        "открой",
        "открой сайт",
    ]
        self.promt = promt

        for i in self.variants:
            if self.promt.lower().find(i) != -1 and self.link.split()[1].find("://") != -1:
                wb.open_new_tab(self.link.split()[1])

class Close:
    def __init__(self, command: str):
        self.command = command
        self.variants = [
            "закрой программу",
            "закрыть программу",
            "заверши программу",
            "завершить программу",
            "останови программу",
            "остановить выполнение",
            "выйди из программы",
            "выйти",
            "выход",
            "завершение работы",
            "прекрати работу",
            "останови процесс",
            "выключись",
            "выключить приложение",
            "отключись",
            "выключись"
        ]

        for i in self.variants:
            if len(self.command.split()) == 3:
                if (self.command.split()[0] + " " + self.command.split()[1] + " " +self.command.split()[2]).lower().find(i) != -1:
                    os._exit(0)
            elif len(self.command.split()) == 2:
                if (self.command.split()[0] + " " + self.command.split()[1]).lower().find(i) != -1:
                    os._exit(0)
            elif len(self.command.split()) == 1:
                if self.command.split()[0].lower().find(i) != -1:
                    os._exit(0)