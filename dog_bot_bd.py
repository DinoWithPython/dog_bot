"""Запись в базу данных для пользователей, что взаимодейтсуют с ботом."""

import pandas as pd
import psycopg
import csv

import config


def __tg_create_table():
    """
    Создает или заменяет таблицу в базе данных PostgreSQL.

    Args:
        config.DB_NAME: Имя базы данных.
        config.DB_USER: Имя пользователя базы данных.
        config.DB_PASSWORD: Пароль пользователя базы данных.
        config.DB_HOST: Хост базы данных.
    Returns:
        None
    """
    with psycopg.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"CREATE TABLE {config.TG_TABLE} "
                "(date_get_dog timestamp with time zone DEFAULT now(), "
                "user_telegram_id BIGINT, user_name VARCHAR(300));"
            )
            conn.commit()


def __vk_create_table():
    """
    Создает или заменяет таблицу в базе данных PostgreSQL.

    Args:
        config.DB_NAME: Имя базы данных.
        config.DB_USER: Имя пользователя базы данных.
        config.DB_PASSWORD: Пароль пользователя базы данных.
        config.DB_HOST: Хост базы данных.
    """
    with psycopg.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"CREATE TABLE {config.VK_TABLE} "
                "(date_get_dog timestamp with time zone DEFAULT now(), "
                "user_vk_id BIGINT, user_name VARCHAR(300));"
            )
            conn.commit()


def vk_add_record(user_vk_id, name):
    """
    Добавляет запись в базу данных.

    Args:
        user_vk_id: Идентификатор пользователя в VK.
        name: Имя пользователя.

    Returns:
        None
    """
    with psycopg.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"INSERT INTO {config.VK_TABLE}"
                " (user_vk_id, user_name) VALUES (%s, %s)",
                (user_vk_id, name),
            )
            conn.commit()


def tg_add_record(user_telegram_id, name):
    """
    Добавляет запись в базу данных.

    Args:
        user_telegram_id: Идентификатор пользователя в Telegram.
        name: Имя пользователя.

    Returns:
        None
    """
    with psycopg.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"INSERT INTO {config.TG_TABLE}"
                " (user_telegram_id, user_name) VALUES (%s, %s)",
                (user_telegram_id, name),
            )
            conn.commit()


def get_table_columns(table: str) -> list:
    """По названию таблицы возвращает заголовки этой таблицы в виде списка."""
    with psycopg.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
            f"""SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
            AND table_name = '{table}';""")
            data = [x[0] for x in cur.fetchall()]
        return data


def records_to_csv(table: str):
    """
    Выгружает все данные из базы данных в CSV-файл.

    Returns:
        None
    """
    with psycopg.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {table}")
            data = cur.fetchall()
            df = pd.DataFrame(
                data, columns=get_table_columns(table)
            )
            df.to_csv(f"{table}.csv", index=False)
        print("Данные сохранены в файл.", f"{table}.csv")


def read_csv_and_put_bd(table: str):
    """Читает данные из csv файла и загружает данные в таблицу."""
    headers = get_table_columns(table)

    with psycopg.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
    ) as conn:
        with open (f"{table}.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            with conn.cursor() as cur:
                for row in reader:
                    cur.execute(
                        f"INSERT INTO {table} ({','.join(headers)}) "
                        "VALUES (%s, %s, %s)",
                        row
                    )
        conn.commit()
        print(f"Записи добавлены в таблицу {table}.")
