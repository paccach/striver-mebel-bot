from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import database as db
from keyboards import inline
from states import CostSG

router = Router()


@router.message(Command("add_cost", "rem_cost"))
async def start_cost(message: Message, state: FSMContext):
    projects = await db.get_projects()
    if not projects:
        return await message.answer("Список пуст")

    if "add" in message.text:
        sign = 1
    else:
        sign = -1
    await state.update_data(sign=sign)

    await state.set_state(CostSG.selecting_project)
    await message.answer("Выберите объект:", reply_markup=inline.project_kb(projects, "cost_p"))


@router.callback_query(F.data.startswith("cost_p:"), CostSG.selecting_project)
async def select_category(call: CallbackQuery, state: FSMContext):
    p_id = int(call.data.split(":")[1])
    await state.update_data(p_id=p_id)
    await call.message.edit_text("Выберите категорию:", reply_markup=inline.category_kb(p_id, "cost_c"))


@router.callback_query(F.data.startswith("cost_c:"))
async def ask_amount(call: CallbackQuery, state: FSMContext):
    p_id = call.data.split(":")[1]
    cat_idx = call.data.split(":")[2]
    await state.update_data(cat_idx=int(cat_idx), p_id=int(p_id))
    await state.set_state(CostSG.entering_amount)
    await call.message.edit_text("Введите сумму:")


@router.message(CostSG.entering_amount)
async def save_cost(message: Message, state: FSMContext):
    if not message.text.replace('.', '', 1).isdigit():
        return await message.answer("Нужно число")

    data = await state.get_data()
    amount = float(message.text) * data['sign']

    await db.update_cost(data['p_id'], data['cat_idx'], amount)
    await message.answer("✅ Данные обновлены")
    await state.clear()