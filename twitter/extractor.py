# twitter から DL してきた過去のツイート (tweets.js) から、ツイートのみを抽出し1行ずつ output.txt に出力する
import re


is_reply = re.compile(r'"@[0-9a-zA-Z_]+\s')

# js フォーマットから文字列のみ抜き出す
def cleanse(text: str) -> str:
    # ツイートのみを取り出す
    ret = text.replace('"full_text" : ', '')
    ret = re.search(r'"(.*)"', ret).group() + "\n"

    # リプライなら @ を先頭から削除していく
    while re.match(is_reply, ret):
        ret = re.sub(is_reply, '"', ret)

    # 改行と二重引用符を全角スペースと一重引用符に置換する
    ret = re.sub(r'\\n', '　', ret)
    ret = re.sub(r'\\"', "'", ret)

    # 先頭の空白を全て消す
    ret = re.sub(r'"[\s　]+', '"', ret)
    return ret[1:-1] + "\n"


def has_urls(text: str) -> bool:
    return "http" in text


def is_retweet(text: str) -> bool:
    return "RT @" in text


# path で与えられたファイルを開き、ツイートを収拾する
def extract_from_tweets_js(path: str) -> list[str]:
    results = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if "full_text" in line and not has_urls(line) and not is_retweet(line):
                tweet_text = cleanse(line)
                if (not '@' in tweet_text) and len(tweet_text) > 12:
                    results.append(tweet_text)
    return results


def main():
    results = extract_from_tweets_js("data/tweets.js")
    with open("output.txt", "w", encoding="utf-8") as f:
        f.writelines(results)


if __name__ == "__main__":
    main()
