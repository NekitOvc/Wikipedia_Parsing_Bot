import requests
from bs4 import BeautifulSoup
from logger import setup_logging

logger = setup_logging()

class ParserUrl:
    url = "https://ru.wikipedia.org/w/index.php?go=Перейти&search="

    def parser_url(self, url):
        self.response = requests.get(url)
        logger.info(f"Статус подключения: {self.response.status_code}")

        soup = BeautifulSoup(self.response.text, "html.parser")
        link = soup.find_all("div", class_="mw-search-result-heading")

        if len(link) > 0:
            url = "https://ru.wikipedia.org" + link[0].find("a")["href"]