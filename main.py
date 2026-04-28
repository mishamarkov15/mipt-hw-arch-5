import requests
from collections import Counter


def get_text(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def iter_words(text):
    start = None
    for index, char in enumerate(text):
        if char.isspace():
            if start is not None:
                yield text[start:index]
                start = None
        elif start is None:
            start = index

    if start is not None:
        yield text[start:]


def count_word_frequencies(text, words_to_count):
    target_words = set(words_to_count)
    frequencies = Counter()

    for word in iter_words(text):
        if word in target_words:
            frequencies[word] += 1

    return {word: frequencies[word] for word in words_to_count}

def main():
    words_file = "words.txt"
    url = "https://eng.mipt.ru/why-mipt/"

    with open(words_file, 'r') as file:
        words_to_count = list(dict.fromkeys(
            word
            for line in file
            if (word := line.strip())
        ))

    text = get_text(url)
    frequencies = count_word_frequencies(text, words_to_count)
    
    print(frequencies)

if __name__ == "__main__":
    main()
