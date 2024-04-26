import argparse

def main(path: str) -> None:
    text = read_book(path)
    word_count = count_words(text)
    print(word_count)

def read_book(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def count_words(text: str) -> int:
    return len(text.split())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--book', action='store')
    args = parser.parse_args()

    main(args.book)
