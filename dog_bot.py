import re

from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram.error import NetworkError

import config
from dog_bot_bd import tg_add_record
from get_dog import get_new_image

updater = Updater(token=config.TG_TOKEN)


def new_dog(update, context):
    """
    Функция отправляет случайное изображение собаки в чат.

    Args:
        update: Объект обновления, содержащий информацию о сообщении.
        context: Объект контекста, содержащий информацию о боте и чате.

    Returns:
        None
    """
    chat = update.effective_chat
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    try:
        context.bot.send_photo(chat.id, get_new_image())
        tg_add_record(chat.id, f"{first_name} {last_name}")
    except NetworkError:
        context.bot.send_photo(chat.id, get_new_image())
        tg_add_record(chat.id, f"{first_name} {last_name}")


def wake_up(update, context):
    """
    Функция отправляет приветственное сообщение и изображение
    собаки пользователю, а также добавляет запись в базу данных.

    Args:
        update: Объект обновления, содержащий информацию о сообщении.
        context: Объект контекста, содержащий информацию о боте и чате.

    Returns:
        None
    """
    chat = update.effective_chat
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    # За счёт параметра resize_keyboard=True сделаем кнопки поменьше
    button = ReplyKeyboardMarkup([["НюДог"]], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text=(
            f"Привет, {first_name}. Ты успешно меня "
            "гавтивировал. Посмотри, какого песеля я тебе нашёл"),
        reply_markup=button,
    )
    tg_add_record(chat.id, f"{first_name} {last_name}")

    context.bot.send_photo(chat.id, get_new_image())


def main():
    """
    Основная функция бота.

    Returns:
        None
    """
    updater.dispatcher.add_handler(CommandHandler("start", wake_up))
    updater.dispatcher.add_handler(CommandHandler("newdog", new_dog))
    regex_pattern = re.compile(r"^(НюДог)$", re.IGNORECASE)
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text & Filters.regex(regex_pattern), new_dog)
    )

    for user in config.USERS:
        updater.dispatcher.bot.send_message(user, config.INFORM)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
