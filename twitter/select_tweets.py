import re

def has_multi_char(input: str, threshold: int = 3) -> bool:
    count: map[str, int] = {}
    for char in input:
        count[char] = count.get(char, 0) + 1
    # threshold より多い文字があれば True
    for c in count.values():
        if c > threshold:
            return True
    return False


def has_ascii_char(input: str, threshold: int = 5) -> bool:
    return len(re.findall("[\x20-\x7E]", input)) >= threshold


def main():
    results = []
    with open("shapa/result.txt", "r", encoding="utf-8") as f:
        for line in f:
            if not has_multi_char(line) and (not has_ascii_char(line)):
                results.append(line)
    with open("output.txt", "w", encoding="utf-8") as f:
        f.writelines(results)


# has_ascii_char のテストをする関数
def has_ascii_char_test():
    assert has_ascii_char("あいうえおabcd") == False
    assert has_ascii_char("あいうえおabcde") == True
    assert has_ascii_char("abcde") == True
    assert has_ascii_char("(292--)") == True


if __name__ == "__main__":
    main()
