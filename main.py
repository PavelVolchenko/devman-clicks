import os
import requests
from dotenv import load_dotenv


def shorten_link(headers, url):
    payload = {"long_url": url}
    response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, json=payload)
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
    response = requests.get(url, headers=headers)
    return response.ok


if __name__ == '__main__':
    load_dotenv()
    headers = {
        'Authorization': f'Bearer {os.environ["BITLY_TOKEN"]}',
    }
    link = input('Введите ссылку: ')
    try:
        if is_bitlink(headers, link):
            print(count_clicks(headers, link))
        else:
            print(shorten_link(headers, link))
    except requests.exceptions.HTTPError as msg:
        print(f"{msg.response.json()['description']} {msg.response.json()['message']}")

