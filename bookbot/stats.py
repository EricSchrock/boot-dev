from typing import Dict

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
