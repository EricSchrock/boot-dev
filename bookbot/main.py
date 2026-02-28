import sys
from typing import Dict

from stats import count_words, count_letters

def main(path: str) -> None:
    text = read_book(path)
    word_count = count_words(text)
    letter_count = count_letters(text)
    print_report(path, word_count, letter_count)

def read_book(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def print_report(path: str, word_count: int, letter_count: Dict[str, int]):
    letter_count = {k: v for k, v in sorted(letter_count.items(), key=lambda item: item[1], reverse=True)}

    print(f"--- Begin report of {path} ---")
    print(f"Found {word_count} total words")
    print()
    print("Found the following letters")
    for k, v in letter_count.items():
        print(f"{k}: {v}")
    print(f"--- End report of {path} ---")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <path_to_book>")
        sys.exit(1)

    main(sys.argv[1])
