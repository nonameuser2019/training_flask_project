import requests
from bs4 import BeautifulSoup
import lxml
from datetime import datetime

from webapp.model import  db, News


link = 'https://www.python.org/'


def get_html(link):
    try:
        page = requests.get(link)
        page.raise_for_status()
        return page.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def get_python_news():
    page = get_html(link)
    soup = BeautifulSoup(page, 'lxml')
    news = soup.find('div', class_='shrubbery').find('ul', class_='menu').find_all('li')
    for row in news:
        title = row.find('a').text
        url = row.find('a')['href']
        published = row.find('time').text
        try:
            published= datetime.strptime(published, '%Y-%m-%d')
        except (ValueError):
            published = datetime.now()
        save_news(title, url, published)

def save_news(title, url, published):
    news_exists = News.query.filter(News.url == url).count()
    print(news_exists)
    if not news_exists:
        new_news = News(title=title, url=url, published=published)
        db.session.add(new_news)
        db.session.commit()





