from pprint import pprint
from urllib.parse import urlencode, urlparse, parse_qs
from config import TOKEN
import requests


def shorten_link(token, url):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }
    data = '{ "long_url": "' + url + '", "domain": "bit.ly", "group_guid": "BnahnqHJgFb" }'
    response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, data=data)
    response.raise_for_status()
    bitlink = response.json()['id']
    return bitlink


def count_clicks(token, link):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary'
    query_args = {
        'unit': 'day',
        'units': '-1',
    }
    encoded_args = urlencode(query_args, doseq=True)
    response = requests.get(url + "?" + encoded_args, headers=headers)
    response.raise_for_status()
    link_clicks = response.json()['total_clicks']
    return link_clicks


if __name__ == '__main__':
    link = input('Введите ссылку: ')
    try:
        bitlink = shorten_link(TOKEN, link)
    except requests.exceptions.HTTPError as msg:
        print(msg.response.json()['description'])
    else:
        print("Битлинк:", bitlink)
        try:
            link_clicks = count_clicks(TOKEN, bitlink)
        except requests.exceptions.HTTPError as msg:
            print(msg.response.json()['description'])
        else:
            print("Кликов:", link_clicks)
