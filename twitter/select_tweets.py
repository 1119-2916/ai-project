def has_multi_char(input: str, threshold: int = 5) -> bool:
    count: map[str, int] = {}
    for char in input:
        count[char] = count.get(char, 0) + 1
    # threshold より多い文字があれば True
    for c in count.values():
        if c > threshold:
            return True
    return False


def main():
    results = []
    with open("shapa/result.txt", "r", encoding="utf-8") as f:
        for line in f:
            if not has_multi_char(line) and len(line) > 40:
                results.append(line)
    with open("output.txt", "w", encoding="utf-8") as f:
        f.writelines(results)


if __name__ == "__main__":
    main()
