import requests
from decouple import config

from main import get_file_extension
from main import download_image

"""
APOD: Astronomy Picture of the Day
"""


def get_spacex_last_captured_launch_id():
    response = requests.get('https://api.spacexdata.com/v5/launches')
    response.raise_for_status()

    for launch in reversed(response.json()):
        if len(launch["links"]["flickr"]["original"]):
            return launch["id"]


def main():
    params = {
        'api_key': config('NASA_API_KEY'),
        'count': 30,
        'thumbs': 'true'
    }

    try:
        response = requests.get('https://api.nasa.gov/planetary/apod', params=params)
        response.raise_for_status()

        for image_number, image_data in enumerate(response.json(), 1):
            image_url = image_data['url']
            download_image(image_url, 'images/nasa_apod_' + str(image_number) + get_file_extension(image_url))
    except requests.exceptions.HTTPError as error:
        raise SystemExit(f'Произошла ошибка:\n{error}')


if __name__ == '__main__':
    main()
