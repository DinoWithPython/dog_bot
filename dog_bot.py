import requests
import os

from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater
from telegram.error import NetworkError

from dotenv import load_dotenv

from dog_bot_bd import add_record

load_dotenv()

secret_token = os.getenv('TOKEN')

updater = Updater(token=secret_token)

URL_dog = 'https://api.thedogapi.com/v1/images/search'
URL_dog_alt = 'https://dog.ceo/api/breeds/image/random'

inform = "Привет! Я гавтивирован."

def get_new_image():
    try:
        response = requests.get(URL_dog).json()
        random_dog = response[0].get('url')
    except Exception as e:
        print(f'Возникла ошибка: {e} \n- перехожу в альтернативный источник.')
        response = requests.get(URL_dog_alt).json()
        random_dog = response.get('message')
    return random_dog

def new_dog(update, context):
    chat = update.effective_chat
    try:
        context.bot.send_photo(
            chat.id,
            get_new_image()
        )
        add_record(chat.id)
    except NetworkError:
        context.bot.send_photo(
            chat.id,
            get_new_image()
        )
        add_record(chat.id)

def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    # За счёт параметра resize_keyboard=True сделаем кнопки поменьше
    button = ReplyKeyboardMarkup([['/newdog']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Ты успешно меня гавтивировал. Посмотри, какого песеля я тебе нашёл'.format(name),
        reply_markup=button
    )
    add_record(chat.id)

    context.bot.send_photo(chat.id, get_new_image())

updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(CommandHandler('newdog', new_dog))

for user in (os.getenv('user_1_for_notif'), os.getenv('user_2_for_notif')):
    updater.dispatcher.bot.send_message(
        user,
        inform
    )

updater.start_polling()
updater.idle()
