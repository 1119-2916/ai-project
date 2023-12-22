import json
import logging
import os
import re

logging.basicConfig(level=logging.INFO)


def logging_messages(pre_text: str, data: list[str]) -> None:
    for i in data:
        logging.info(pre_text + i)


def remove_parenthesis(data: str) -> str:
    pattern = r"<.*>\s?"
    return re.sub(pattern, "", data)


def extract_message(data: list[tuple[str, str]]) -> list[str]:
    result: list[str] = []
    for author, message in data:
        # url を含まない black_99rose の発言を抽出する
        if author == "black_99rose" and "http" not in message:
            message = message.replace("\n", " ").replace("　", " ")
            message = remove_parenthesis(message)
            if len(message) == 1:
                continue
            result.append(message)
    return result


# chat_log/*.txt の全てについて、ファイルを読み込み、json を整形して、特定の発言を取り出します
def read_chat_log() -> list[str]:
    result: list[str] = []
    files = os.listdir("./chat_log")
    for filename in files:
        logging.info(f"Reading {filename}")
        if filename == ".gitignore" or filename == "dj-omaera.txt":
            continue
        with open(f"./chat_log/{filename}") as f:
            data = json.load(f)
            messages = extract_message(data)
            result.extend(messages)
            logging_messages(filename, messages)
            logging.info(f"finish reading {filename}, {len(messages)} messages were extracted!")
    return result


def main():
    with open("./train_data/train_data.json", "w") as f:
        json.dump(read_chat_log(), f, ensure_ascii=False)


if __name__ == "__main__":
    main()
