from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import database as db
from config import CATEGORIES
from states import MebelSG
from keyboards import inline

router = Router()


@router.message(Command("add_mebel"))
async def start_add(message: types.Message, state: FSMContext):
    await state.set_state(MebelSG.name)
    await message.answer("Введите название изделия:")


@router.message(MebelSG.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text, values=[])
    await state.set_state(MebelSG.values)
    await message.answer(f"Введите плановую стоимость для:\n<b>{CATEGORIES[0]}</b>", parse_mode="HTML")


@router.message(MebelSG.values)
async def get_values(message: types.Message, state: FSMContext):
    if not message.text.replace('.', '', 1).isdigit():
        return await message.answer("Введите число:")

    data = await state.get_data()
    vals = data['values']
    vals.append(float(message.text))

    if len(vals) < len(CATEGORIES):
        await state.update_data(values=vals)
        next_cat = CATEGORIES[len(vals)]
        await message.answer(f"Введите плановую стоимость для:\n<b>{next_cat}</b>", parse_mode="HTML")
    else:
        name=data['name']
        success = await db.add_project(name, vals)
        if success:
            await message.answer(f"✅ Проект '{name}' успешно создан!")
        else:
            await message.answer("❌ Ошибка: проект с таким именем уже есть.")
        await state.clear()


@router.message(Command("delete"))
async def list_to_delete(message: types.Message):
    projects = await db.get_projects()
    if not projects:
        return await message.answer("Список проектов пуст.")

    await message.answer(
        "Выберите проект для <b>удаления</b>:",
        reply_markup=inline.project_kb(projects, "del"),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("del:"))
async def process_delete(call: types.CallbackQuery):
    p_id = int(call.data.split(":")[1])
    await db.delete_project(p_id)
    await call.answer("Проект удален", show_alert=True)
    await call.message.delete()