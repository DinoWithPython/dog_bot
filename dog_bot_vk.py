import requests

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.upload import VkUpload

import config
from get_dog import get_new_image
from dog_bot_bd import vk_add_record

# Инициализация
vk_session = vk_api.VkApi(token=config.VK_TOKEN)
longpoll = VkBotLongPoll(vk_session, config.VK_GROUP)
vk = vk_session.get_api()
upload = VkUpload(vk_session)


def upload_photo(image_url):
    """
    Загружает изображение на сервер VK.

    Args:
        image_url: URL изображения.

    Returns:
        str: Строка для отправки вложения.
    """
    # Скачиваем изображение
    image = requests.get(image_url, stream=True)
    image.raw.decode_content = True

    # Загружаем изображение на сервер VK
    photo = upload.photo_messages(photos=image.raw)[0]

    # Возвращаем строку для отправки вложения
    return f"photo{photo['owner_id']}_{photo['id']}"


# Обработка событий
def main():
    """
    Основная функция для работы со скриптом. Прослушивает сообщения.

    При получении сообществом сообщения с любым текстом, бот отвечает
    сообщением "Привет, [Имя] [Фамилия]!" и описывает возможности бота.

    При получении сообщения с текстом "НюДог", бот получает новое
    изображение собаки и отправляет его пользователю.
    """
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            message = event.object.message
            user_id = message["from_id"]
            text = message["text"]
            user_info = vk.users.get(
                user_ids=user_id,
                fields="first_name,last_name"
                )[0]
            first_name = user_info["first_name"]
            last_name = user_info["last_name"]

            # Ответ на сообщение
            if text.lower() == "привет":
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("НюДог", color=VkKeyboardColor.POSITIVE)
                vk.messages.send(
                    user_id=user_id,
                    message=(
                        "Я гавтивирован.\n\n Чтобы получить дога"
                        " - жмакни по кнопке НюДог."
                        "Так же я запостю дога в ленту группы"
                        " и мы все сможем любоваться этим красавчиком."
                    ),
                    keyboard=keyboard.get_keyboard(),
                    random_id=0,
                )
            elif text.lower() == "нюдог":
                # Получаем URL изображения собаки
                image_url = get_new_image()

                # Загружаем изображение и получаем attachment
                attachment = upload_photo(image_url)

                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button("НюДог", color=VkKeyboardColor.POSITIVE)
                vk.messages.send(
                    user_id=user_id,
                    message="Вот НюДог!",
                    attachment=attachment,
                    keyboard=keyboard.get_keyboard(),
                    random_id=0,
                )
                vk_add_record(
                    user_vk_id=user_id,
                    name=f"{first_name} {last_name}"
                    )
            else:
                vk.messages.send(
                    user_id=user_id,
                    message=(
                        f'Привет, {first_name} {last_name}!'
                        ' Напиши мне "привет", если хочешь узнать что я умею.'
                    ),
                    random_id=0,
                )


if __name__ == "__main__":
    main()
