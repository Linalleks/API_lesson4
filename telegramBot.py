import telegram
from decouple import config


def main():
    bot = telegram.Bot(token=config('TG_BOT_TOKEN'))
    channel_id = '@space_photos_linalleks'
    # bot.send_message(text='Тестовый Привет на канале "Космические фотки(т)"', chat_id=channel_id)
    # bot.send_document(chat_id=channel_id, document=open('images/hubble.jpeg', 'rb'))
    # bot.send_photo(chat_id=channel_id, photo=open('images/hubble.jpeg', 'rb'))
    bot.send_photo(chat_id=channel_id, photo='https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg')


if __name__ == '__main__':
    main()
