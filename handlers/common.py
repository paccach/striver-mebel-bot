from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "<b>Система учета мебельного производства</b>\n\n"
        "Команды:\n"
        "/add_mebel — новый проект\n"
        "/add_cost — добавить расход\n"
        "/rem_cost — вычесть расход\n"
        "/view — список всех объектов\n"
        "/delete — удалить проект\n\n"
        "Для отмены любого ввода напишите /cancel",
        parse_mode="HTML"
    )

@router.message(Command("cancel"))
async def cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Действие отменено.")