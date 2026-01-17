import argparse
import os
import random

import telegram
from decouple import config

from helper_scripts import get_all_files_paths
from helper_scripts import image_reduction


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('image_path', nargs='?')

    return parser


def main():
    parser = create_parser()
    bot = telegram.Bot(token=config('TG_BOT_TOKEN'))
    channel_id = config('TG_CHANNEL_ID')
    max_size = 10485760

    if parser.parse_args().image_path:
        image = parser.parse_args().image_path
    else:
        image = random.choice(get_all_files_paths('images'))

    if os.path.getsize(image) > max_size:
        new_image = image_reduction(image, max_size)
        image = new_image
    bot.send_photo(chat_id=channel_id, photo=open(image, 'rb'))


if __name__ == '__main__':
    main()
