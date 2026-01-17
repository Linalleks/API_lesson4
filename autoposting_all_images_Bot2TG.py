import os
import random
from time import sleep

import telegram
from decouple import config
from pytimeparse import parse

from helper_scripts import get_all_files_paths
from helper_scripts import compress_image


def main():
    bot = telegram.Bot(token=config('TG_BOT_TOKEN'))
    channel_id = config('TG_CHANNEL_ID')
    set_delay = parse(config('SET_DELAY', default='4h'))
    max_size = 10485760
    images_paths = get_all_files_paths('images')

    while True:
        for number, image in enumerate(images_paths):
            if os.path.getsize(image) > max_size:
                new_image = compress_image(image, max_size)
                images_paths[number] = new_image
                image = new_image
            bot.send_photo(chat_id=channel_id, photo=open(image, 'rb'))
            sleep(set_delay)
        random.shuffle(images_paths)


if __name__ == '__main__':
    main()
