#encoding: utf-8

import argparse
from collections import Counter

import pymongo
import pymorphy2
from nltk.tokenize import RegexpTokenizer
from wordcloud import WordCloud
from stop_words import get_stop_words


TOKENIZER = RegexpTokenizer(r'\w+')
MORPH = pymorphy2.MorphAnalyzer()
STOPS = get_stop_words('ru')


def count_words(text):
    result_count = Counter()
    tokens = [MORPH.parse(token)[0].normal_form for token in TOKENIZER.tokenize(text)]
    tokens_no_stops = [token for token in tokens if token not in STOPS]
    result_count.update(tokens_no_stops)
    return result_count


def main(chat_id):
    content = pymongo.MongoClient()['ai_parody_storage']['content']

    print('For chat', chat_id)

    all_messages_from_chat = content.find({'chat': {'id': chat_id}})
    word_counters = {'all': Counter()}
    for msg in all_messages_from_chat:
        if msg.get('text', msg.get('caption')) is not None:
            text = msg.get('text', msg.get('caption'))
            counts = count_words(text)
            word_counters['all'] += counts
            user_id = msg.get('from', {}).get('id', 'error')
            if user_id not in word_counters:
                word_counters[user_id] = Counter()
            word_counters[user_id] += counts

    print('Saving pics.')

    for user_id, c in word_counters.items():
        # Docs: https://amueller.github.io/word_cloud/
        wc = WordCloud(width=1000, height=1000)
        wc.generate_from_frequencies(list(c.items()))
        wc.to_file('wcs/' + str(user_id) + '.png')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--chat_id', type=int)
    args = parser.parse_args()
    main(args.chat_id)
