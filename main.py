import requests
from bs4 import BeautifulSoup
import re
import random
import genanki
import itertools
from model import chinese_vocab_model

def get_endpoint():
    try: 
        set_number = int(input("enter hsk vocab set # (1-6): "))
        if (set_number < 0) or (set_number > 6):
            raise Exception("[x] hsk vocab set # must be >= 1 and <= 6")
        return f'https://hsk.academy/en/hsk-{set_number}-vocabulary-list'
    except Exception as e:
        print(f'[x] input exception: {e}')
        return ''

def request_html(endpoint):
    try:
        r = requests.get(endpoint)
        if r.status_code != 200:
            raise Exception('[x] request exception: bad status code')
        return r.text
    except Exception as e:
        print(f'[x] request exception: {e}')
        return ''

class VocabWord:
    def __init__(self, word, pinyin, meaning):
        self.word = word
        self.pinyin = pinyin
        self.meaning = meaning

def parse_html(html):
    try:
        vocab_list = []
        soup = BeautifulSoup(html, 'html.parser')
        for tr in soup.find_all('tr'):
            strings = tr.find('a').get_text().splitlines()
            word = strings[0].strip()
            pinyin = strings[1].strip()
            meaning = re.sub(r'\s+', ' ', tr.find('td', attrs={'class': None}).get_text()).strip()
            vocab_list.append(VocabWord(word, pinyin, meaning))
        return vocab_list
    except Exception as e:
        print(f'[x] parse excpetion: {e}')
        return []

colors = ['#3498db', '#e74c3c', '#2ecc71', '#9b59b6']
color_cycle = itertools.cycle(colors)

def colorize_chinese_and_pinyin(word, pinyin):
    chars = list(word)
    pinyin_parts = pinyin.split(" ")

    colored_word = ''
    colored_pinyin = ''

    for char, py in zip(chars, pinyin_parts):
        color = next(color_cycle)
        colored_word += f'<span style="color:{color}">{char}</span>'
        colored_pinyin += f'<span style="color:{color}">{py}</span> '

    return colored_word.strip(), colored_pinyin.strip()

def generate_deck(vocal_list, deck_name):
    try:
        my_deck = genanki.Deck(
            random.randrange(1 << 30, 1 << 31),
            deck_name
        )
        for vocab in vocab_list:
            color_word, color_pinyin = colorize_chinese_and_pinyin(vocab.word, vocab.pinyin)
            note = genanki.Note(
                model = chinese_vocab_model,
                fields = [
                    vocab.word, 
                    vocab.meaning,
                    color_word,
                    color_pinyin
                ]
            )
            my_deck.add_note(note)
        genanki.Package(my_deck).write_to_file(f'{deck_name}.apkg')
    except Exception as e:
        print('[x] generation exception: {e}')

if __name__ == '__main__':
    print()

    endpoint = get_endpoint()
    if not endpoint:
        raise Exception('[x] input exception: endpoint not set')
    print() # \n for nicer logs
    print(f'[+] endpoint obtained: {endpoint}')

    html = request_html(endpoint)
    if not html:
        raise Exception('[x] request exception: html not set')
    print('[+] obtained hsk.academy vocal list html')

    vocab_list = parse_html(html)
    if not vocab_list:
        raise Exception('[x] parse exception: vocab_list not set')
    print('[+] parsed hsk.academy vocal list html')
    print() # \n for nicer logs

    deck_name = input("deck name (e.x. 'HSK 1 Vocab'): ")
    if not deck_name:
        raise Exception('[x] provide a deck name')
    print() # \n for nicer logs

    generate_deck(vocab_list, deck_name)
    print(f'[+] generated \'{deck_name}\' deck in this folder as \'{deck_name}.apkg\'')
    print( '[!] to open this deck open the anki app and drag the .apkg file into anki')
