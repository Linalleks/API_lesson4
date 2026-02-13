from pathlib import Path
import requests
from decouple import config

from helper_scripts import download_image
from helper_scripts import get_file_extension

"""
APOD: Astronomy Picture of the Day
"""


def main():
    params = {
        'api_key': config('NASA_API_KEY'),
        'count': 30,
        'thumbs': 'true'
    }

    response = requests.get('https://api.nasa.gov/planetary/apod', params=params)
    response.raise_for_status()

    for image_number, image_data in enumerate(response.json(), 1):
        if image_data['media_type'] == 'video':
            image_url = image_data['thumbnail_url']
        else:
            image_url = image_data['url']
        download_image(image_url, Path('images') / f'nasa_apod_{image_number}{get_file_extension(image_url)}')


if __name__ == '__main__':
    main()
