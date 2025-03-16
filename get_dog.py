import requests

URL_dog = 'https://api.thedogapi.com/v1/images/search'
URL_dog_alt = 'https://dog.ceo/api/breeds/image/random'

def get_new_image() -> str:
    """
    Функция получает случайное изображение собаки из API.

    В случае возникновения ошибки при запросе к первому источнику,
    функция переходит к альтернативному источнику.

    Returns:
        str: URL случайного изображения собаки.
    """
    try:
        response = requests.get(URL_dog).json()
        random_dog = response[0].get('url')
    except Exception as e:
        print(f'Возникла ошибка: {e} \n- перехожу в альтернативный источник.')
        response = requests.get(URL_dog_alt).json()
        random_dog = response.get('message')
    return random_dog