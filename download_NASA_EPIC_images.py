from pathlib import Path
import requests

from helper_scripts import download_image

"""
EPIC: Earth Polychromatic Imaging Camera
"""


def main():
    try:
        response = requests.get('https://epic.gsfc.nasa.gov/api/natural/all')
        response.raise_for_status()
        epic_dates = response.json()[:10]

        for image_number, epic_date in enumerate(epic_dates, 1):
            response = requests.get('https://epic.gsfc.nasa.gov/api/natural/date/' + epic_date['date'])
            response.raise_for_status()
            epic_image = response.json()[0]['image'] + '.png'
            image_url = 'https://epic.gsfc.nasa.gov/archive/natural/' + epic_date['date'].replace('-', '/') + '/png/' + epic_image
            download_image(image_url, Path('images') / f'nasa_epic_{image_number}.png')
    except requests.exceptions.HTTPError as error:
        raise SystemExit(f'Произошла ошибка:\n{error}')


if __name__ == '__main__':
    main()
