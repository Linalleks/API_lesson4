import telegram
from decouple import config


def main():
    bot = telegram.Bot(token=config('TG_BOT_TOKEN'))
    bot.send_message(text='Тестовый Привет на канале "Космические фотки(т)"', chat_id='@space_photos_linalleks')


if __name__ == '__main__':
    main()
