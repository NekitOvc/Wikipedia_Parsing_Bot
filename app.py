# -*- coding: utf-8 -*-
import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config import AllConfigurations
from logger import setup_logging
from parser_url import ParserUrl
from connect_db import db_connection, new_user, table_articles, recording_responce

load_dotenv(".env.local")
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

logger = setup_logging()

@dp.message(Command("start"))
async def command_start(message: types.Message):
    """Обработка команды /start"""
    logger.info(f"Пользователь {message.from_user.full_name} активировал бота")
    await bot.send_message(message.from_user.id, AllConfigurations.welcome_text)
    logger.info(f"Бот отправил приветственное сообщение пользователю {message.from_user.full_name}")
    await db_connection()
    await new_user(user_id=message.from_user.id, user_name=message.from_user.full_name)
    await table_articles()

@dp.message()
async def send_wiki(message: types.Message):
    """Функция получения статьи из wiki"""
    logger.info(f"Пользователь {message.from_user.full_name} ввёл сообщение {message.text}")
    user_request = ParserUrl.url + message.text
    await bot.send_message(message.from_user.id, AllConfigurations.link_to_website)
    await bot.send_message(message.from_user.id, f'<a href="{user_request}">Нажимай</a>', parse_mode="HTML")
    logger.info(f"Полльзователь {message.from_user.full_name} получил сообщение со ссылкой {user_request}")
    await recording_responce(value=message.text, url=user_request)

async def start_polling():
    try:
        print("Осуществлён запуск бота")
        logger.info("Осуществлён запуск бота")
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        print("Polling был отменен.")
        logger.warning("Polling был отменен.")
    except KeyboardInterrupt:
        print("Бот остановлен.")
        logger.warning("Бот остановлен.")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start_polling())