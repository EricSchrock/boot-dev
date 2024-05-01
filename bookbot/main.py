import argparse
from typing import Dict

def main(path: str) -> None:
    text = read_book(path)
    word_count = count_words(text)
    letter_count = count_letters(text)
    print_report(path, word_count, letter_count)

def read_book(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def count_words(text: str) -> int:
    return len(text.split())

def count_letters(text: str) -> Dict[str, int]:
    text = text.lower()
    letter_count = {}
    for c in text:
        if c.isalpha():
            if not c in letter_count:
                letter_count[c] = 0
            letter_count[c] += 1
    return letter_count

def print_report(path: str, word_count: int, letter_count: Dict[str, int]):
    letter_count = {k: v for k, v in sorted(letter_count.items(), key=lambda item: item[1], reverse=True)}

    print(f"--- Begin report of {path} ---")
    print(f"{word_count} words found in the document")
    print()
    for k, v in letter_count.items():
        print(f"The '{k}' character was found {v} times")
    print("--- End report ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--book', action='store')
    args = parser.parse_args()

    main(args.book)
