import os
import requests
from urllib.parse import urlencode, urlparse
from dotenv import load_dotenv


def shorten_link(headers, url):
    data = '{ "long_url": "' + url + '", "domain": "bit.ly", "group_guid": "BnahnqHJgFb" }'
    response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, data=data)
    response.raise_for_status()
    bitlink = response.json()['id']
    return bitlink


def count_clicks(headers, link):
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


def is_bitlink(url):
    headers = {
        'Authorization': f'Bearer {os.environ["TOKEN"]}',
        'Content-Type': 'application/json',
    }
    parsed_url = urlparse(url)
    if parsed_url.path.split('/')[0] == 'bit.ly':
        try:
            return f"Кликов: {count_clicks(headers, parsed_url.path)}"
        except requests.exceptions.HTTPError as msg:
            return f"{msg.response.json()['description']} {msg.response.json()['message']}"
    else:
        try:
            return f"Битлинк: {shorten_link(headers, url)}"
        except requests.exceptions.HTTPError as msg:
            return f"{msg.response.json()['description']} {msg.response.json()['message']}"


if __name__ == '__main__':
    load_dotenv()
    link = input('Введите ссылку: ')
    print(is_bitlink(link))
