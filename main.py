import requests
import os

from urllib.parse import urlparse
from urllib.parse import unquote


def download_image(image_url, download_path):
    response = requests.get(image_url, headers={'User-Agent': 'Mozilla/5.0 (compatible; HandsomeBrowser/1.2)'})
    response.raise_for_status()

    os.makedirs(os.path.dirname(download_path), exist_ok=True)

    with open(download_path, 'wb') as file:
        file.write(response.content)


def get_file_extension(image_url):
    split_url = urlparse(image_url)
    image_path = unquote(split_url.path)
    image_extension = os.path.splitext(image_path)[1]

    return image_extension


def main():
    download_image("https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg", 'images/hubble.jpeg')


if __name__ == '__main__':
    main()
