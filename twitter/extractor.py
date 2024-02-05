# twitter から DL してきた過去のツイート (tweets.js) から、ツイートのみを抽出し1行ずつ output.txt に出力する
import re
import sys


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

    # バックスラッシュは jsonl だとフォーマットエラーになるので消す
    ret = re.sub(r'\\', "＼", ret)

    # 先頭の空白を全て消す
    ret = re.sub(r'"[\s　]+', '"', ret)
    return ret[1:-1] + "\n"


def has_urls(text: str) -> bool:
    return "http" in text


def is_retweet(text: str) -> bool:
    return "RT @" in text


# path で与えられたファイルを開き、ツイートを収拾する
# めちゃくちゃ適当に特定の年以降のものだけ抽出するように実装した
def extract_from_tweets_js(path: str, time: int) -> list[str]:
    results = []
    target: bool = False
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if "created_at" in line:
                inner_target = False
                for year in range(time, 2025):
                    if str(year) in line:
                        inner_target = True
                        break
                target = inner_target
            if target and "full_text" in line and not has_urls(line) and not is_retweet(line):
                tweet_text = cleanse(line)
                if '@' in line and (not '@' in tweet_text) and len(tweet_text) > 1:
                    results.append(tweet_text)
    return results


def main():
    if len(sys.argv) <= 1:
        print("no argument. you must specify input file path.")
        return

    input_path = sys.argv[1]
    results = extract_from_tweets_js(input_path, 2022)
    with open("output.txt", "w", encoding="utf-8") as f:
        f.writelines(results)


if __name__ == "__main__":
    main()
