import requests
import os
from PIL import Image
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


def image_reduction(image_path, max_size):
    with Image.open(image_path, 'r') as source:
        quality = 100
        new_image_path = os.path.splitext(image_path)[0] + '(resize).jpg'
        source.save(new_image_path, quality=quality, optimize=True, progressive=True)
        while os.path.getsize(new_image_path) > max_size:
            quality -= 1
            source.save(new_image_path, quality=quality, optimize=True, progressive=True)
    return new_image_path


def get_all_files_paths(files_dir):
    files_paths = []
    for dirpath, dirnames, filenames in os.walk(files_dir):
        if dirpath == files_dir:
            for image in filenames:
                files_paths.append(dirpath.replace('\\', '/') + '/' + image)
        else:
            for image in filenames:
                files_paths.append(dirpath.replace('\\', '/') + '/' + image)
    return files_paths
