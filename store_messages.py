#encoding: utf-8

import argparse
import time

import telepot
import pymongo
import yaml


def store_content(content):
    collection = pymongo.MongoClient()['ai_parody_storage']['content']
    collection.insert_one(content)


def store_metadata(data):
    collection = pymongo.MongoClient()['ai_parody_storage']['metadata']
    if collection.find_one({'id': data['id']}) is None:
        collection.insert_one(data)
    else:
        pass


def handle(msg):
    meta_data = []
    meta_data.append(msg['from'])
    meta_data.append(msg['chat'])

    content_part = msg.copy()
    content_part['chat'] = {'id': msg['chat']['id']}
    content_part['from'] = {'id': msg['from']['id']}

    if content_part.get('forward_from_chat') is not None:
        meta_data.append(content_part['forward_from_chat'])
        content_part['forward_from_chat'] = {'id': content_part['forward_from_chat']['id']}

    if content_part.get('forward_from') is not None:
        meta_data.append(content_part['forward_from'])
        content_part['forward_from'] = {'id': content_part['forward_from']['id']}

    if content_part.get('reply_to_message') is not None:
        meta_data.append(content_part['reply_to_message']['from'])
        content_part['reply_to_message']['from'] = {'id': content_part['reply_to_message']['from']['id']}
        meta_data.append(content_part['reply_to_message']['chat'])
        content_part['reply_to_message']['chat'] = {'id': content_part['reply_to_message']['chat']['id']}



    store_content(content_part)
    for data in meta_data:
        store_metadata(data)


def do_work(telegram_token):
    bot = telepot.Bot(telegram_token)
    bot.message_loop(handle)
    while 42:
        time.sleep(10)


def main(config_filename):
    with open(config_filename) as config_file:
        config = yaml.load(config_file.read())
        do_work(config['telegram_token'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='default.yml')
    args = parser.parse_args()
    main(args.config)
