import requests
from bs4 import BeautifulSoup
import lxml
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
    all_news = []
    page = get_html(link)
    soup = BeautifulSoup(page, 'lxml')
    news = soup.find('div', class_='shrubbery').find('ul', class_='menu').find_all('li')
    for row in news:
        all_news.append({'title': row.find('a').text, 'url': row.find('a')['href'], 'time': row.find('time').text})
    return all_news


def main():
    all_news = get_python_news()
    print(all_news)

if __name__ == '__main__':
    main()




