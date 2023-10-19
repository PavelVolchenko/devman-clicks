import os
import requests
from dotenv import load_dotenv


def shorten_link(headers, url):
    long_url = '{"long_url":"' + url + '"}'
    response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, data=long_url)
    response.raise_for_status()
    bitlink = response.json()['id']
    return bitlink


def count_clicks(headers, link):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary'
    payload = {
        'unit': 'day',
        'units': '-1',
    }
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    link_clicks = response.json()['total_clicks']
    return link_clicks


def is_bitlink(headers, link):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return True
    except:
        return False


if __name__ == '__main__':
    load_dotenv()
    headers = {
        'Authorization': f'Bearer {os.environ["TOKEN"]}',
    }
    link = input('Введите ссылку: ')
    if is_bitlink(headers, link):
        try:
            print(count_clicks(headers, link))
        except requests.exceptions.HTTPError as msg:
            f"{msg.response.json()['description']} {msg.response.json()['message']}"
    else:
        try:
            print(shorten_link(headers, link))
        except requests.exceptions.HTTPError as msg:
            f"{msg.response.json()['description']} {msg.response.json()['message']}"
