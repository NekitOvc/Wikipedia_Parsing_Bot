# Wikipedia_Parsing_Bot
https://t.me/Wikipedia_Parsing_Bot - бот, который получает запрос пользователя, парсит сайт https://ru.wikipedia.org/, получает необходимую статью и отправляет её пользователю. 

Используемые библиотеки:

- aiogram
- requests
- beautifulsoup
- logging
- emoji
- sqlite3

Реализовано логирование в файл py_log.log и создание базы данных db.db с двумя таблицами:

1. users - таблица пользователей, работающих с ботом
2. articles - список ссылок, отправленных пользователю
