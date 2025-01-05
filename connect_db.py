import aiosqlite
from logger import setup_logging

logger = setup_logging()

async def db_connection():
    """Подключение к БД и создание таблицы пользователей"""
    global connection, cursor
    try:
        connection = await aiosqlite.connect("db.db")
        cursor = await connection.cursor()
        logger.info("Подключение к БД произошло успешно")

        await cursor.execute("CREATE TABLE IF NOT EXISTS users(user_id TEXT PRIMARY KEY, name TEXT)")
        await connection.commit()
        logger.info("Создана таблица users")
    except Exception as e:
        logger.error(f"Ошибка подключения к БД: {e}")
    finally:
        if connection:
            await connection.close()

async def new_user(user_id, user_name):
    """Запись нового пользователя в БД"""
    try:
        async with aiosqlite.connect("db.db") as connection:
            cursor = await connection.cursor()
            user = await cursor.execute("SELECT 1 FROM users WHERE user_id == ?", (user_id,))
            user_exists = await user.fetchone()

            if not user_exists:
                await cursor.execute("INSERT INTO users VALUES(?, ?)", (user_id, user_name))
                await connection.commit()
                logger.info(f"Пользователь {user_name} успешно внесён в БД")
    except Exception as e:
        logger.error(f"Ошибка при записи нового пользователя: {e}")

async def table_articles():
    """Создание таблицы со статьями"""
    try:
        async with aiosqlite.connect("db.db") as connection:
            cursor = await connection.cursor()
            await cursor.execute("CREATE TABLE IF NOT EXISTS articles(value TEXT, url TEXT)")
            await connection.commit()
            logger.info("Создана таблица articles")
    except Exception as e:
        logger.error(f"Ошибка при создании таблицы articles: {e}")

async def recording_responce(value, url):
    """Запись статьи в БД"""
    try:
        async with aiosqlite.connect("db.db") as connection:
            cursor = await connection.cursor()
            await cursor.execute("INSERT INTO articles VALUES(?, ?)", (value, url))
            await connection.commit()
            logger.info("Статья успешно внесена в БД")
    except Exception as e:
        logger.error(f"Ошибка при записи статьи: {e}")