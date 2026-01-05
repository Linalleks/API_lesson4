import requests
import os
from decouple import config
from urllib.parse import urlparse
from urllib.parse import unquote
# import argparse


def download_image(image_url, download_path):
    response = requests.get(image_url, headers={'User-Agent': 'Mozilla/5.0 (compatible; HandsomeBrowser/1.2)'})
    response.raise_for_status()

    os.makedirs(os.path.dirname(download_path), exist_ok=True)

    with open(download_path, 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch():
    response = requests.get('https://api.spacexdata.com/v5/launches/5eb87ce3ffd86e000604b336')
    response.raise_for_status()

    for image_number, image_url in enumerate(response.json()["links"]["flickr"]["original"], 1):
        download_image(image_url, 'images/spacex_' + str(image_number) + get_file_extension(image_url))


def fetch_nasa_APODs(api_key):
    """
    APOD: Astronomy Picture of the Day
    """
    params = {
        'api_key': api_key,
        'count': 30,
        'thumbs': 'true'
    }
    response = requests.get('https://api.nasa.gov/planetary/apod', params=params)
    response.raise_for_status()

    for image_number, image_data in enumerate(response.json(), 1):
        image_url = image_data['url']
        download_image(image_url, 'images/nasa_apod_' + str(image_number) + get_file_extension(image_url))


def get_file_extension(image_url):
    split_url = urlparse(image_url)
    image_path = unquote(split_url.path)
    image_extension = os.path.splitext(image_path)[1]

    return image_extension


def fetch_nasa_EPICs():
    """
    EPIC: Earth Polychromatic Imaging Camera
    """
    response = requests.get('https://epic.gsfc.nasa.gov/api/natural/all')
    response.raise_for_status()
    epic_dates = response.json()[:10]

    for image_number, epic_date in enumerate(epic_dates, 1):
        response = requests.get('https://epic.gsfc.nasa.gov/api/natural/date/' + epic_date['date'])
        response.raise_for_status()
        epic_image = response.json()[0]['image'] + '.png'
        image_url = 'https://epic.gsfc.nasa.gov/archive/natural/' + epic_date['date'].replace('-', '/') + '/png/' + epic_image
        download_image(image_url, 'images/nasa_epic_' + str(image_number) + '.png')


def main():
    download_image("https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg", 'images/hubble.jpeg')
    fetch_spacex_last_launch()
    fetch_nasa_APODs(config('NASA_API_KEY'))
    fetch_nasa_EPICs()


if __name__ == '__main__':
    main()
