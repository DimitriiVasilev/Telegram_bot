import requests
import json
import urllib
from dbhelper import DBHelper


db = DBHelper()

TOKEN = open('TOKEN').read().rstrip()  # bot's token
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


def send_message(chat_id, text, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + f"sendMessage?text={text}&chat_id={chat_id}"
    if reply_markup:
        url += f"&reply_markup={reply_markup}"
    get_url(url)


def handle_updates(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        items = db.get_items(chat)
        if text == "/done":
            keyboard = build_keyboard(items)
            send_message(chat, "Select an item to delete", keyboard)
            continue
        elif text == "/start":
            send_message(
                chat,
                "Welcome to your personal To Do list. Send any text to me and I'll store it as an item. "
                "Send /done to remove items",
                )
        elif text.startswith("/"):
            continue
        elif text in items:
            db.delete_item(text, chat)
            items = db.get_items(chat)
            if items:
                keyboard = build_keyboard(items)
                send_message(chat, "Select an item to delete", keyboard)
            else:
                send_message(chat, 'Write down new list')
        else:
            db.add_item(text, chat)
            items = db.get_items(chat)
            message = "\n".join(items)
            send_message(chat, message)


def build_keyboard(items):
    keyboard = [[key] for key in items]
    reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def show_messages(updates):
    for update in updates['result']:
        message = update['message']['text']
        user = update['message']['chat']['username']
        try:
            print(f'got {message} from {user}')
        except Exception as e:
            print(e)


def main():
    last_update_id = None
    while True:
        db.setup()
        updates = get_updates(last_update_id)
        if len(updates['result']):
            last_update_id = get_last_update_id(updates) + 1
            show_messages(updates)
            handle_updates(updates)


if __name__ == '__main__':
    main()
