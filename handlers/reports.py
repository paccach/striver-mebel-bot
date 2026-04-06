from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import database as db
from config import CATEGORIES
from collections import defaultdict

router = Router()


@router.message(Command("view"))
async def show_report(message: Message):
    projects = await db.get_projects()
    if not projects:
        return await message.answer("Данных пока нет.")

    months = defaultdict(list)
    for p in projects:
        m_key = p['date'][:7]
        months[m_key].append(p)

    for month, p_list in sorted(months.items(), reverse=True):
        msg = [f"<b>ОТЧЕТ ЗА {month}</b>", "═" * 20]

        m_theory = 0
        m_practice = 0

        for p in p_list:
            msg.append(f"\n<b>Объект: {p['name']}</b>")
            p_theory = 0
            p_practice = 0

            for i, cat in enumerate(CATEGORIES):
                t_val = p[f"t_{i}"] or 0
                p_val = p[f"p_{i}"] or 0
                diff = t_val - p_val

                p_theory += t_val
                p_practice += p_val

                if t_val > 0 or p_val > 0:
                    if diff >= 0:
                        status = "✅"
                    else:
                        status = "🔴"
                    msg.append(f"  └ {cat}: {status} {diff:,.0f} руб.")

            p_diff = p_theory - p_practice
            m_theory += p_theory
            m_practice += p_practice

            msg.append(f"  <b>ИТОГО {p['name']}: {p_diff:,.0f} руб.</b>")
            msg.append("─" * 15)

        m_diff = m_theory - m_practice
        if m_diff >= 0:
            m_status = "📈 В плюсе"
        else:
            m_status = "📉 Перерасход"

        msg.append(f"\n<b>ИТОГ МЕСЯЦА {month}:</b>")
        msg.append(f"План: {m_theory:,.0f} | Факт: {m_practice:,.0f}")
        msg.append(f"Результат: <b>{m_diff:,.0f} руб. ({m_status})</b>")

        await message.answer("\n".join(msg), parse_mode="HTML")