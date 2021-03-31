import re
import typing

import requests
import tornado.web
import tornado.ioloop
import json

URL = 'https://raw.githubusercontent.com/RobertJGabriel/Google-profanity-words/master/list.txt'
SYMBOL_TO_REPLACE = '*'
PORT = 4201


def get_words(url: str) -> typing.List[str]:
    req = requests.get(url)
    if req.status_code == requests.codes.ok:
        bad_words = req.text.split('\n')
    else:
        raise ValueError(f'Url "{url}" not found')
    return bad_words


class Filter:
    def __init__(self, worst_words_ever: typing.List[str], replace_symbol: str):
        self.worst_words_ever = sorted(worst_words_ever, key=lambda x: len(x), reverse=True)
        if self.worst_words_ever[-1] == '':
            self.worst_words_ever.pop()
        self.pattern = re.compile('|'.join(map(re.escape, self.worst_words_ever)))
        self.replace_symbol = replace_symbol
        self.sentence: typing.Optional[str] = None

    def add_bad_words(self, list_of_words: typing.List[str]):
        self.worst_words_ever += list_of_words
        self.worst_words_ever.sort(key=lambda x: len(x), reverse=True)

    def _replace_worst_word(self, sre_match) -> str:
        bad_word_in_theory = sre_match.group(0)
        # todo add more complex filtering of bad words
        return re.sub(r'[^ ]', self.replace_symbol, bad_word_in_theory)

    def _return_upper_cases(self, old: str, new: str) -> str:
        return ''.join(map(lambda x, y: x if x.isupper() and y != self.replace_symbol else y, old, new))

    def run(self, input_string: str):
        self.sentence = input_string
        tmp_string = self.pattern.sub(self._replace_worst_word, input_string.lower())
        return self._return_upper_cases(old=input_string, new=tmp_string)

# todo add add endpoint which get array of bad words to add it in filter class
class FilterHandler(tornado.web.RequestHandler):
    def initialize(self, filter_class: Filter):
        self.filter_class: Filter = filter_class

    # for angular cors
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')

    # for angular cors
    def options(self, *args, **kwargs):
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Allow-Methods', '*')
        self.set_status(204)
        self.finish()

    def post(self):
        message = json.loads(self.request.body)['message']
        result = {'message': self.filter_class.run(message)}
        self.write(json.dumps(result))


if __name__ == '__main__':
    words = get_words(URL)
    filter_ = Filter(words, replace_symbol=SYMBOL_TO_REPLACE)

    app = tornado.web.Application([
        (r"/api/filter-bad-words/en-US", FilterHandler, dict(filter_class=filter_)),
    ])

    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()