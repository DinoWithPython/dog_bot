import time
import threading

from dog_bot import main as dog_tg
from dog_bot_vk import main as dog_bot_vk

# Запуск ботов в отдельных потоках
if __name__ == "__main__":
    # Создаем потоки
    telegram_thread = threading.Thread(target=dog_tg, daemon=True)
    vk_thread = threading.Thread(target=dog_bot_vk, daemon=True)

    # Запускаем потоки
    print("Бот в телеге начинает работу")
    telegram_thread.start()
    print("Бот в вк начинает работу.")
    vk_thread.start()

    try:
        # Бесконечный цикл, чтобы основной поток не завершался
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Обработка завершения (Ctrl+C)
        print("Завершение работы ботов...")
        print("Боты завершили работу.")
