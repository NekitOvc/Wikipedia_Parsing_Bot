from bs4 import BeautifulSoup

import requests
import logging

# логирование в файл py_log.log в режиме перезаписи при каждом запуске бота с указанием времени
logging.basicConfig(level=logging.INFO, filename='py_log.log', filemode='w', format='%(asctime)s %(levelname)s %(message)s')

class ParserUrl:
    # url, с которым будем работать
    url = 'https://ru.wikipedia.org/w/index.php?go=Перейти&search='

    def parser_url(url):
        # отправляем get-запрос
        r = requests.get(url)
        # проверка подключения
        logging.info(f'Статус подключения: {r.status_code}')

        soup = BeautifulSoup(r.text, 'html.parser')
        # поиск тега div с классом mw-search-result-heading
        link = soup.find_all('div', class_='mw-search-result-heading')

        # если количество элементов > 0, то
        if len(link) > 0:
            # новая ссылка
            url = 'https://ru.wikipedia.org' + link[0].find('a')['href']