"""Запись в базу данных для пользователей, что взаимодейтсуют с ботом."""

import pandas as pd
import psycopg

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
                f"CREATE OR REPLACE TABLE {config.TG_TABLE} "
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
                f"CREATE OR REPLACE TABLE {config.VK_TABLE} "
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


def tg_records_to_csv():
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
            cur.execute(f"SELECT * FROM {config.TG_TABLE}")
            data = cur.fetchall()
            df = pd.DataFrame(
                data, columns=["date_record", "user_telegram_id", "user_name"]
            )
            df.to_csv(f"{config.TG_TABLE}.csv", index=False)
