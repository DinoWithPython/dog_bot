import os

from dotenv import load_dotenv

load_dotenv()

# TG
TG_TOKEN = os.getenv("TG_TOKEN")
USERS = [os.getenv("USER1"), os.getenv("USER2")]
INFORM = "Привет! Я гавтивирован."
TG_TABLE = "telegram"

# DB
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

# VK
VK_GROUP = os.getenv("VK_GROUP")
VK_TOKEN = os.getenv("VK_TOKEN")
VK_TABLE = os.getenv("VK_TABLE")
