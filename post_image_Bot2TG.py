import argparse
import os
import random

import telegram
from decouple import config

from helper_scripts import get_all_files_paths
from helper_scripts import compress_image


def create_parser():
    parser = argparse.ArgumentParser(description='''
                                     Приложение публикует указанную как аргумент фотографию в Телеграмм-канал.
                                     Если фотография не указана, публикует случайную фотографию из папки "images".
                                     ''')
    parser.add_argument('image_path', nargs='?', help='Относительный путь до фотографии для публикации')

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
        image = compress_image(image, max_size)
    with open(image, 'rb') as p:
        photo = p.read()
    bot.send_photo(chat_id=channel_id, photo=photo)


if __name__ == '__main__':
    main()
