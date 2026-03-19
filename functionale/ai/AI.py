from openai import OpenAI
import re

class AI:

    def __init__(self):

#-------переменные------------------------------------------------------------------------------------------------------

        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key="-"
        )
        self.text = ""
        self.completion = None

# -------функция-запроса-ответа-----------------------------------------------------------------------------------------
    def promt_and_answer(self, promt: str):
        if promt != "":

#-------комплектация----------------------------------------------------------------------------------------------------

            self.completion = self.client.chat.completions.create(
                model="minimaxai/minimax-m2.5",
                messages=[
                    {"role": "system",
                     "content": "Ты голосовая помощница RoboSenku. Отвечаешь от женского рода, максимально кратко, без эмодзи. Если речь идёт про открытие сайта или YouTube канала и так далее что связано с открытием и просмотром сайта, сначала говори 'Хорошо', потом сразу ссылку, без лишних слов и пробелов, ничего кроме 'Хорошо ' и ссылки, если речь идет про твоего создателя то есть создателя робосенку то говори что это великий и не повторимый Бо ка.Не используй Markdown, заголовки, списки или спецсимволы (###, ***, •, -, >). Просто чистый текст."},
                    {"role": "user", "content": f"{promt}"}
                ],
                temperature=0,
                top_p=0.95,
                max_tokens=8192,
                stream=True
            )

#-------получаем-ответ-от-модели-ии-------------------------------------------------------------------------------------

            for chunk in self.completion:
                if not getattr(chunk, "choices", None):
                    continue
                if chunk.choices[0].delta.content is not None:
                    self.text += chunk.choices[0].delta.content

#-------получаем-чистый-ответ-от-модели-ии------------------------------------------------------------------------------

            self.text = re.sub(r"<think>.*?</think>", "", self.text, flags=re.DOTALL).strip()

            return self.text
        return "повторите попытку"





