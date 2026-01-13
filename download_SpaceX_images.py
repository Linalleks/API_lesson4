import requests
import argparse

from helper_scripts import get_file_extension
from helper_scripts import download_image


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('launch_id', nargs='?')

    return parser


def get_spacex_last_captured_launch_id():
    response = requests.get('https://api.spacexdata.com/v5/launches')
    response.raise_for_status()

    for launch in reversed(response.json()):
        if len(launch["links"]["flickr"]["original"]):
            return launch["id"]


def main():
    parser = create_parser()

    try:
        if parser.parse_args().launch_id:
            launch_id = parser.parse_args().launch_id
        else:
            launch_id = get_spacex_last_captured_launch_id()

        response = requests.get('https://api.spacexdata.com/v5/launches/' + launch_id)
        response.raise_for_status()

        for image_number, image_url in enumerate(response.json()["links"]["flickr"]["original"], 1):
            download_image(image_url, 'images/spacex_' + str(image_number) + get_file_extension(image_url))
    except requests.exceptions.HTTPError as error:
        raise SystemExit(f'Произошла ошибка:\n{error}')


if __name__ == '__main__':
    main()
