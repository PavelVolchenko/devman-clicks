from pprint import pprint

from config import TOKEN
import requests
def get_profile(user):
    url = 'https://api-ssl.bitly.com/v4/user'
    headers = {'Authorization': f'Bearer {TOKEN}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


    # headers = {
    #     'Authorization': 'Bearer {TOKEN}',
    #     'Content-Type': 'application/json',
    # }
    #
    # data = '{ "long_url": "https://dev.bitly.com", "domain": "bit.ly", "group_guid": "o_5io4i55lq4" }'
    #
    # response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, data=data)


if __name__ == '__main__':
    pprint(get_profile('xakep'))


