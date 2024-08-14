"""Запись в базу данных для пользователей, что взаимодейтсуют с ботом."""
import os

import pandas as pd
import psycopg
from dotenv import load_dotenv

load_dotenv()

dbname=os.getenv('dbname')
user=os.getenv('user_db')
password=os.getenv('password_db')
host=os.getenv('host_db')

TABLE_NAME = 'data_dog_bot'

def __create_table():
    """Добавление записи в базу данных."""
    with psycopg.connect(dbname=dbname, user=user, password=password, host=host) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"CREATE TABLE {TABLE_NAME} "
                "(date_get_dog timestipe with time zone DEFAULT now(), user_telegram_id BIGINT);")
            conn.commit()

def add_record(user_telegram_id):
    """Добавление записи в базу данных."""
    with psycopg.connect(dbname=dbname, user=user, password=password, host=host) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"INSERT INTO {TABLE_NAME} (user_telegram_id) VALUES (%s)",
                (user_telegram_id,))
            conn.commit()

def records_to_csv():
    """Выгружает все данные из БД в CSV."""
    with psycopg.connect(dbname=dbname, user=user, password=password, host=host) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT * FROM {TABLE_NAME}")
            data = cur.fetchall()
            df = pd.DataFrame(data, columns=['date_record', 'user_telegram_id'])
            df.to_csv(f'{TABLE_NAME}.csv', index=False)
