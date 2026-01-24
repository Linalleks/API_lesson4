import os
from pathlib import Path
from urllib.parse import unquote
from urllib.parse import urlparse

import requests
from PIL import Image


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


def compress_image(image_path, max_size):
    with Image.open(image_path, 'r') as source:
        quality = 100
        new_image_path = os.path.splitext(image_path)[0] + '(resize).jpg'
        source.save(new_image_path, quality=quality, optimize=True, progressive=True)
        while os.path.getsize(new_image_path) > max_size:
            quality -= 1
            source.save(new_image_path, quality=quality, optimize=True, progressive=True)
    return new_image_path


def get_all_files_paths(source_dir):
    files_paths = []
    for current_dir, internal_dirs, files in os.walk(source_dir):
        for file in files:
            files_paths.append(Path(current_dir) / file)
    return files_paths


if __name__ == '__main__':
    # Path.home() / 'python' / 'samples' / 'test_me.py'
    image_number = 1
    image_url = 'https://api.nasa.gov/planetary/apod/124klklll555.png'
    ppp = Path('images') / f'nasa_apod_{image_number}{get_file_extension(image_url)}'
    print(ppp)
