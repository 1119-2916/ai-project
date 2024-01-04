from .ai_client import AIClient
from private.secrets import BOT_ID, OPENAI_API_SECRET, MODEL_ID
from openai import OpenAI

class MeuAI(AIClient):
    prompt: str = """
女子高生として雑談をせよ。
"""

    @property
    def bot_id(self) -> str:
        return BOT_ID["meu"]

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_SECRET)

    def generate_reply(self, message: str) -> str:
        # メッセージが長すぎる場合は無視する
        if len(message) > 100:
            return ""
        # メッセージが短すぎる場合も無視する
        elif len(message) < 4:
            return ""
        else:
            completion = self.client.chat.completions.create(
                model=MODEL_ID["meu"],
                messages=[
                    {"role": "system", "content": self.prompt},
                    {"role": "user", "content": message}
                ]
            )
            return completion.choices[0].message.content

    # メッセージにURLが含まれる場合は無視する
    def generate_reply_to_including_URL(self, message: str) -> str:
        return ""

    # メッセージに画像が含まれる場合は無視する
    def generate_reply_to_including_image(self, message: str) -> str:
        return ""
