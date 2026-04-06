from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import CATEGORIES

def project_kb(projects, prefix: str):
    kb = InlineKeyboardBuilder()
    for p in projects:
        kb.button(text=p['name'], callback_data=f"{prefix}:{p['id']}")
    kb.adjust(2)
    return kb.as_markup()

def category_kb(p_id: int, prefix: str):
    kb = InlineKeyboardBuilder()
    for idx, name in enumerate(CATEGORIES):
        kb.button(text=name, callback_data=f"{prefix}:{p_id}:{idx}")
    kb.adjust(2)
    return kb.as_markup()