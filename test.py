import requests
import json
import time
import urllib


TOKEN = '649261804:AAFxq5igPWZ0N0WyGwLfuA8LCsne275APVc'
URL = f'https://api.telegram.org/bot{TOKEN}/'


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += f'&offset={offset}'
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    return max([int(update['update_id']) for update in updates['result']])


def send_message(chat_id, text):
    text = urllib.parse.quote_plus(text)
    url = URL + f"sendMessage?text={text}&chat_id={chat_id}"
    get_url(url)


def echo_all(updates):
    for update in updates['result']:
        try:
            text = update['message']['text']
            chat_id = update['message']['chat']['id']
            send_message(chat_id, text)
        except Exception as e:
            print(e)


def show_messages(updates):
    for update in updates['result']:
        try:
            print(update['message']['text'], ' from ', update['message']['chat']['username'])
        except Exception as e:
            print(e)


def main():
    last_update_id = None
    while True:
        print("getting updates")
        updates = get_updates(last_update_id)
        if len(updates['result']):
            last_update_id = get_last_update_id(updates) + 1
            show_messages(updates)
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
