import argparse
from pathlib import Path

import requests

from helper_scripts import download_image
from helper_scripts import get_file_extension


def create_parser():
    parser = argparse.ArgumentParser(description='''
                                     Приложение скачивает фото от SpaceX по указанному как аргумент ID запуска.
                                     Если ID запуска не указан, скачивает фото с последнего запуска с имеющимися фото.
                                     ''')
    parser.add_argument('launch_id', nargs='?', help='ID запуска SpaceX')

    return parser


def get_spacex_last_captured_launch_id():
    response = requests.get('https://api.spacexdata.com/v5/launches')
    response.raise_for_status()

    for launch in reversed(response.json()):
        if len(launch["links"]["flickr"]["original"]):
            return launch["id"]


def main():
    parser = create_parser()

    if parser.parse_args().launch_id:
        launch_id = parser.parse_args().launch_id
    else:
        launch_id = get_spacex_last_captured_launch_id()

    response = requests.get(f'https://api.spacexdata.com/v5/launches/{launch_id}')
    response.raise_for_status()

    for image_number, image_url in enumerate(response.json()["links"]["flickr"]["original"], 1):
        download_image(image_url, Path('images') / f'spacex_{image_number}{get_file_extension(image_url)}')


if __name__ == '__main__':
    main()
