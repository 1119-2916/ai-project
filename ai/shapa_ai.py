import time
from private.secrets import BOT_ID, OPENAI_API_SECRET, MODEL_ID, PROMPTS
from .ai_client import AIClient
from openai import OpenAI

class ShapaAI(AIClient):
    prompt: str = PROMPTS["shapa"]

    @property
    def bot_id(self) -> str:
        return BOT_ID["shapa"]

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_SECRET)
        self.history = []

    def _get_history(self) -> str:
        ret = ""
        now = time.time()
        for m, t in self.history:
            if now - t < 60 * 5:
                ret += m
        return ret

    def _push_history(self, question: str, response: str, threshold: int = 3):
        message = f"user:{question}\nassistant: {response}\n"
        self.history.append((message, time.time()))
        while len(self.history) > threshold:
            self.history.pop(0)

    def generate_reply(self, message: str) -> str:
        # メッセージが長すぎる場合は無視する
        if len(message) > 100:
            return ""
        # メッセージが短すぎる場合も無視する
        elif len(message) < 4:
            return ""
        else:
            history = self._get_history()
            if history != "":
                history = "過去には以下のような会話をしています。\n" + history
            completion = self.client.chat.completions.create(
                model=MODEL_ID["shapa"],
                messages=[
                    {"role": "system", "content": self.prompt + history},
                    {"role": "user", "content": message}
                ]
            )
            response = completion.choices[0].message.content
            self._push_history(message, response)
            return response

    # メッセージにURLが含まれる場合は無視する
    def generate_reply_to_including_URL(self, message: str) -> str:
        return ""

    # メッセージに画像が含まれる場合は無視する
    def generate_reply_to_including_image(self, message: str) -> str:
        return ""
