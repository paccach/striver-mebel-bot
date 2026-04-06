import aiosqlite
from config import DB_PATH, CATEGORIES


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        t_cols = ", ".join([f"t_{i} REAL DEFAULT 0" for i in range(len(CATEGORIES))])
        p_cols = ", ".join([f"p_{i} REAL DEFAULT 0" for i in range(len(CATEGORIES))])

        await db.execute(f"""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                {t_cols}, {p_cols}
            )
        """)
        await db.commit()


async def get_projects():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM projects ORDER BY date DESC") as cursor:
            return await cursor.fetchall()


async def add_project(name: str, values: list):
    async with aiosqlite.connect(DB_PATH) as db:
        cols = ", ".join([f"t_{i}" for i in range(len(CATEGORIES))])
        placeholders = ", ".join(["?" for _ in values])
        try:
            await db.execute(
                f"INSERT INTO projects (name, {cols}) VALUES (?, {placeholders})",
                [name] + values
            )
            await db.commit()
            return True
        except:
            return False


async def update_cost(p_id: int, cat_idx: int, amount: float):
    async with aiosqlite.connect(DB_PATH) as db:
        col = f"p_{cat_idx}"
        await db.execute(f"UPDATE projects SET {col} = {col} + ? WHERE id = ?", (amount, p_id))
        await db.commit()


async def delete_project(p_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM projects WHERE id = ?", (p_id,))
        await db.commit()