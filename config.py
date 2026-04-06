import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
DB_PATH = "furniture.db"

CATEGORIES = [
    "ДСП", "Фурнитура", "Разное", "Сборка", "Доставка",
    "Дизайнер", "Технолог", "Менеджер1", "Менеджер2",
    "Производство", "Реклама", "Транспорт", "Налог"
]