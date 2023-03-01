from aiogram import Bot, Dispatcher, executor, types
from config import AllConfigurations
from parser_url import ParserUrl
from connect_db import db_connection, new_user, table_articles, recording_responce

import logging

# инициализация бота
bot = Bot(token=AllConfigurations.TOKEN)
dp = Dispatcher(bot)

# логирование в файл py_log.log в режиме перезаписи при каждом запуске бота с указанием времени
logging.basicConfig(level=logging.INFO, filename='py_log.log', filemode='w', format='%(asctime)s %(levelname)s %(message)s')

# обработка команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    logging.info(f'Пользователь {message.from_user.full_name} активировал бота')
    await bot.send_message(message.from_user.id, AllConfigurations.welcome_text)
    logging.info(f'Бот отправил приветственное сообщение пользователю {message.from_user.full_name}')
    await db_connection()
    await new_user(user_id=message.from_user.id, user_name=message.from_user.full_name)
    await table_articles()

# обработка ввода текста пользователем
@dp.message_handler(content_types=['text'])
async def send_wiki(message: types.Message):
    logging.info(f'Пользователь {message.from_user.full_name} ввёл сообщение {message.text}')
    # итоговый запрос пользователя, который состоит из заданной ссылки на сайт + введенный текст
    user_request = ParserUrl.url + message.text
    await bot.send_message(message.from_user.id, AllConfigurations.link_to_website)
    await bot.send_message(message.from_user.id, f'<a href="{user_request}">Нажимай</a>', parse_mode='HTML')
    logging.info(f'Полльзователь {message.from_user.full_name} получил сообщение со ссылкой {user_request}')
    await recording_responce(value=message.text, url=user_request)

# бот не отвечает на сообщения, которые были отправлены, когда бот был оффлайн
executor.start_polling(dp, skip_updates=True)