# ファインチューニングした GPT3.5 turbo と会話する discord bot の実験

## ファインチューニングのデータフォーマット

https://openai.com/blog/gpt-3-5-turbo-fine-tuning-and-api-updates

```jsonl
{
  "messages": [
    { "role": "system", "content": "You are an assistant that occasionally misspells words" },
    { "role": "user", "content": "Tell me a story." },
    { "role": "assistant", "content": "One day a student went to schoool." }
  ]
}
```

## 各種結果

| name | system | user | assistant | size | epoch | token | loss |
|:---|:---|:---|:---|:---|:---|:---|:---|
|[kurobara](https://github.com/1119-2916/ai-project?tab=readme-ov-file#kurobara)|✖|✖|〇|1046| 3 | 78,384 | 1.7354 |
|[ikeda](https://github.com/1119-2916/ai-project?tab=readme-ov-file#ikeda)|✖|✖|〇|47823| 1 | 1,740,019 | 2.0195 |
|[meu](https://github.com/1119-2916/ai-project?tab=readme-ov-file#meu)|✖|〇|〇|159| 3 | 72,792 | 1.7384 |
|[shapa](https://github.com/1119-2916/ai-project?tab=readme-ov-file#shapa)|〇|✖|〇|1488| 3 | ? | ? |

### kurobara

```jsonl
{
  "messages": [
    { "role": "assistant", "content": "アキバ来るオタクみんな何時くらいに来る？" }
  ]
}
```

- discord での発言を収拾した
- system, user のフィールドは無し
- assistant に発言を入れたのみ
- 本人の口調を捉えつつ、日本語ややり取りが崩壊していない。成功と言って良い結果。

### ikeda

```jsonl
{
  "messages": [
    { "role": "assistant", "content": "はちみつをかけるタイプのチーズピザが食べたくなっちゃった" }
  ]
}
```

- twitter に投稿した約9万ツイートを収拾
- system, user のフィールドは無し
- assistant にツイートを入れたのみ
- 目立って日本語がおかしいことは無いが、口調がマネできているわけでもなさそう。

### meu

```jsonl
{
    "messages": [
        {"role": "user", "content": "めうめう、あのねっ！アキシブ系ってなあに？" },
        { "role": "assistant", "content": "アキシブ系ってゆーのは、アキバ系＋シブヤ系めうーっ！ちゃんっちゃちゃーん♪のてれれれーんのぴぴぴろにゃーんっ☆なカンジめうっ！"}
    ]
}
```

- [ひなビタのサイト](https://p.eagate.573.jp/game/bemani/hinabita/p/bittersweets/special/talk_4.html?n=4) から収拾
- 会話形式になっているデータである。
- system のフィールドは無し
- user, assistant にデータを入れた
- めう語が非常に難解であったせいか分からないが、日本語が崩壊してしまった。
- なぜか、userであるまり花の口調も混ざっている気がする。
- 失敗

![めうbot](img/meu_bot.png)

### shapa

```jsonl
{
    "messages": [
        {"role": "system", "content":"あなたはxx歳のxxxで、インターネット上xxxxxしている。 日本のxxxxで生まれ育ち、今はxxxxx。一人称は「」と「」を使い分ける。 砕けた敬語を使い、仲良く気さくに話してくれる。 斜に構えたような冗談や、場を茶化すような発言を好む。 返答の文章量は最大で40文字程度であるが、xxxやxxxなどに関係する話題の際は発言の量が60文字程度に増える。 "},
        {"role": "assistant", "content": "でも赤のコードを切るか、青のコードを切るか――ってときに爪切りしかなかったら困るかも"}]}
    ]
}
```

- 全十数万ツイートの中から、40文字以上100文字以下であり、同一の文字を5個以上含まないもの1500件
- 「うおおおおお！！！！！」などは弾かれるということ
- プロンプトはちょっとあからさまだったのでここでは隠したが、実際には入れている
- system のフィールドにプロンプトを、assistant にツイートを入れ、 user は無し
-

## 動作環境
python 3.12
poetry 1.7

# Makefile 解説
## requirements:
poetry で requirements を吐き出す

## install:
poetry で .venv を生成する

## run:
discord bot を実行する

## generate_dataset:
train_data_generator を実行する。plane text などから学習用のフォーマットにしたファイルを吐き出す

## validate_format:
公式から提供されている学習用 jsonl のバリデータ。トークン数も分かる

## upload:
open ai に jsonl をアップロードする

## tuning:
open ai にアップロードした jsonl を元に、ファインチューニングを実行する
