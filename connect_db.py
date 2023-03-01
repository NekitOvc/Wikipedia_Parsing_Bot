import sqlite3
import logging

# подключение БД
async def db_connection():
    global connection, cursor
    connection = sqlite3.connect('db.db')
    cursor = connection.cursor()
    logging.info('Подключение к БД произошло успешно')

    # если таблицы users не существует, создать её
    cursor.execute('CREATE TABLE IF NOT EXISTS users(user_id TEXT PRIMARY KEY, name TEXT)')
    connection.commit()
    logging.info('Создана таблица users')

# запись нового пользователя
async def new_user(user_id, user_name):
    user = cursor.execute('SELECT 1 FROM users WHERE user_id == "{key}"'.format(key=user_id)).fetchone()

    # если пользователя не существует в БД
    if not user:
        # осуществляется запись в БД
        cursor.execute('INSERT INTO users VALUES(?, ?)', (user_id, user_name))
        connection.commit()
        logging.info(f'Пользователь {user_name} успешно внесён в БД')

async def table_articles():
    # если таблицы articles не существует, создать её
    cursor.execute('CREATE TABLE IF NOT EXISTS articles(value TEXT, url TEXT)')
    connection.commit()
    logging.info('Создана таблица articles')

async def recording_responce(value, url):
    cursor.execute('INSERT INTO articles VALUES(?, ?)', (value, url))
    connection.commit()
    logging.info('Статья успешно внесена в БД')