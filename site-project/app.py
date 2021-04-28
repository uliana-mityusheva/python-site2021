from flask import Flask
from flask import render_template
from bs4 import BeautifulSoup
from flask import request
import requests

app = Flask(__name__)

PROXY_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Ubuntu Chromium/55.0.2883.87 Chrome/55.0.2883.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8,uk;q=0.6,ru;q=0.4',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1'
}

main_file = 'index.html'


@app.route('/')
def index():
    template = 'index.html'

    url = 'https://www.championat.com/'

    response = requests.get(url, headers=PROXY_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    item = soup.find_all("a", class_="news-item__title")
    time = soup.find_all("div", class_="news-item__time")
    data = zip(item, time)

    times = []
    title = []
    reference = []

    for link, hour in zip(item, time):
        times.append(hour.text)
        title.append(link.text)
        reference.append(url + link.get('href'))

    table = zip(times, title, reference)
    return render_template(template, table=table)


if __name__ == '__main__':
    app.run()
