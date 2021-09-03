import json
import os
import shutil
from typing import Tuple

import requests


def get_decs_and_image_url_by_url(url: str) -> Tuple[str, str]:
    """
    Get message (username, tagged users and description) and image url

    :param url: instagram url like https://www.instagram.com/p/CR6PEm8HQ_C/
    :return: message and image url
    """

    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        data = requests.get(f'{url.split("?")[0]}?__a=1', headers=headers)
        data_json = json.loads(data.text)

        user_name = data_json['graphql']['shortcode_media']['owner']['username']
        desc = data_json['graphql']['shortcode_media']['edge_media_to_caption']['edges'][0]['node']['text']
        url = data_json['graphql']['shortcode_media']['display_url']
        tagged = [x['node']['user']['username'] for x in data_json['graphql']['shortcode_media']['edge_media_to_tagged_user']['edges']]

        message = f'user: {user_name}\ntagged: {", ".join(tagged)}\ndesc: {desc}'
        return message, url
    except:
        return 'something wrong', ''


def download_image_by_url(image_url: str) -> str:
    """
    Download image from image url

    :param image_url: image url like https://....jpg
    :return: filename or None
    """
    filename = os.path.join('images', image_url.split("/")[-1].split('?')[0])
    os.makedirs('images', exist_ok=True)
    response = requests.get(image_url, stream=True)
    print(filename)
    if response.status_code == 200:
        response.raw.decode_content = True

        with open(filename, 'wb') as f:
            shutil.copyfileobj(response.raw, f)

        return filename
    else:
        return ''


if __name__ == '__main__':
    message_, url_ = get_decs_and_image_url_by_url('https://www.instagram.com/p/CSxFUJRDzTS/')
    ret = download_image_by_url(url_)
