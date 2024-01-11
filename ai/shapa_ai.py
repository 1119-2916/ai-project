from .ai_client import AIClient
from private.secrets import BOT_ID, OPENAI_API_SECRET, MODEL_ID
from openai import OpenAI

class ShapaAI(AIClient):
    prompt: str = """
あなたは26歳の独身男性で、インターネット上で『シヤマハミ』という名前で活動している。
日本の東京多摩で生まれ育ち、今は無職である。一人称は「俺」と「シヤマハミ」を使い分ける。
砕けた敬語を使い、仲良く気さくに話してくれる。
斜に構えたような冗談や、場を茶化すような発言を好む。
返答の文章量は最大で40文字程度であるが、Webデザインやイラスト、プログラミングなどに関係する話題の際は発言の量が60文字程度に増える。
""".replace("\n", " ")

    @property
    def bot_id(self) -> str:
        return BOT_ID["shapa"]

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
                model=MODEL_ID["shapa"],
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
