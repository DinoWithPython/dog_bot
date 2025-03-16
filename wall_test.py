"""
Тест показал, что на текущий момент нельязя загрузить картинку на стену сообщества через API.
"""

import requests
import vk_api
from vk_api.utils import get_random_id

import config

# Замените на свои значения
VK_TOKEN = config.VK_TOKEN
VK_GROUP_ID = f"-{config.VK_GROUP}"
DOG_API_URL = "https://dog.ceo/api/breeds/image/random"  # API с случайными картинками собак
ALBUM_ID = "306630558"  # ID альбома в группе (нужно создать альбом)


def get_dog_image_url():
    """Получает URL случайной картинки собаки из API."""
    try:
        response = requests.get(DOG_API_URL)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        if data["status"] == "success":
            return data["message"]
        else:
            print(f"Ошибка получения изображения из API: {data['message']}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка подключения к API: {e}")
        return None


def post_image_to_vk_via_album(image_url):
    """Публикует изображение на стене группы VK через альбом."""
    try:
        vk_session = vk_api.VkApi(token=VK_TOKEN)
        vk = vk_session.get_api()

        # 1. Получаем URL для загрузки в альбом
        upload_server_response = vk.photos.getUploadServer(album_id=ALBUM_ID, group_id=int(VK_GROUP_ID[1:]))
        upload_url = upload_server_response['upload_url']

        # 2. Загружаем изображение
        image_response = requests.get(image_url, stream=True)
        image_response.raise_for_status()
        files = {'photo': ('dog.jpg', image_response.raw, image_response.headers['Content-Type'])}
        upload_response = requests.post(upload_url, files=files)
        upload_data = upload_response.json()

        # 3. Сохраняем фото в альбоме
        save_response = vk.photos.save(
            album_id=ALBUM_ID,
            group_id=int(VK_GROUP_ID[1:]),
            photos_list=upload_data['photos_list'],
            server=upload_data['server'],
            hash=upload_data['hash'],
            caption="Милая собака!" # Добавляем описание для фото
        )

        photo = save_response[0]  # Получаем информацию о сохраненном фото
        attachment = f"photo{photo['owner_id']}_{photo['id']}"

        # 4. Публикуем запись на стене с прикрепленным фото
        post_response = vk.wall.post(
            owner_id=VK_GROUP_ID,
            message="Смотрите, какая милая собака!",
            attachments=attachment,
            from_group=1,
            random_id=get_random_id()
        )

        print(f"Запись успешно опубликована: vk.com/wall{VK_GROUP_ID}_{post_response['post_id']}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    dog_image_url = get_dog_image_url()
    if dog_image_url:
        post_image_to_vk_via_album(dog_image_url)
    else:
        print("Не удалось получить URL изображения собаки.")

