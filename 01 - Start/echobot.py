import time
import json 
import requests
import urllib
import settings

TOKEN = settings.get_token()
URL = 'https://api.telegram.org/bot{}/'.format(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode('utf-8')
    print('CONTENT:\n', content)
    return content

def get_json_form_url(url):
    content = get_url(url)
    js = json.loads(content)
    print('JS:\n', js)
    return js

def get_updates(offset=None):
    url = URL + 'getUpdates?timeout=100'
    if offset:
        url += '&offset={}'.format(offset)
    js = get_json_form_url(url)
    print(js)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates['result']:
        update_ids.append(int(update['update_id']))
    return max(update_ids)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates['result'])
    last_update = num_updates - 1
    text = updates['result'][last_update]['message']['text']
    chat_id = updates['result'][last_update]['message']['chat']['id']
    return text, chat_id

def echo_all(updates):
    for update in updates['result']:
        try:
            text = update['message']['text']
            chat = update['message']['chat']['id']
            send_message(text, chat)
        except Exception as e:
            print(e)

def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates['result']) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()