import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from config import TOKEN
import database as db
from handlers import common, manage, costs, reports


async def main():
    logging.basicConfig(level=logging.INFO)
    await db.init_db()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_routers(
        common.router,
        manage.router,
        costs.router,
        reports.router
    )

    await bot.set_my_commands([
        types.BotCommand(command="start", description="Инструкция"),
        types.BotCommand(command="add_mebel", description="Новая мебель"),
        types.BotCommand(command="add_cost", description="Добавить расход"),
        types.BotCommand(command="rem_cost", description="Вычесть расход"),
        types.BotCommand(command="view", description="Отчет по месяцам"),
        types.BotCommand(command="delete", description="Удалить проект"),
    ])

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())