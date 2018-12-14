from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
import json
import urllib3
import scrapy
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SECRET_KEY']='edgardeng'
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    message = request.args.get('msg')
    return render_template('index.html', message=message)


@app.route('/weather')
def weather():
    api_url = 'http://www.weather.com.cn/data/sk/101020100.html'
    http = urllib3.PoolManager()
    # 通过request()方法创建一个请求：
    r = http.request('GET', api_url)
    data = r.data.decode()  # urllib3.request.urlopen(api_url).read().decode("utf8")
    result = json.loads(data)
    api_result = result['weatherinfo']

    page_result = ''
    page_url = 'http://www.weather.com.cn/weather/101020100.shtml'
    page = http.request('GET', page_url).data.decode()
    tg_start = page.find('id=\"7d\"')
    if tg_start == -1:
        print('not find start tag')
    else:
        tmp = page[tg_start:-1]
        tg_end = tmp.find('weatherChart')
        page_result = tmp
        if tg_end == -1:
            print('not find end tag')
        else:
            tmp2 = tmp[:tg_end]
            tag_script = tmp2.find('<script>')
            tmp3 = tmp2[:tag_script]
            page_result = '<div ' + tmp3
    return render_template('weather.html', api_url=api_url, api_result=api_result, page_url=page_url, page_result=page_result)


@app.route('/movie')
def movie():
    http = urllib3.PoolManager()
    page_url = 'http://www.mtime.com'
    page = http.request('GET', page_url).data.decode()
    response = scrapy.Selector(text=page)
    sub_movie = response.xpath('//div[@class="ciname-movie"]')
    sub_select = sub_movie[0].xpath('.//dd')
    movies = []
    for sub in sub_select:
        typea = sub.xpath('.//div[@class="smalltypebox"]')
        type = typea.xpath('./p/text()').extract()
        name = sub.xpath('./h3/a/text()').extract()
        item = {
            'name': name,
            'type': type
        }
        movies.append(item)
    return render_template('movie.html', movies=movies)


@app.route('/boxoffice')
def boxoffice():
    http = urllib3.PoolManager()
    page_url = 'http://movie.mtime.com/boxoffice/'
    page = http.request('GET', page_url).data.decode()
    soup = BeautifulSoup(page, 'html.parser')
    # print soup.prettify()
    list = soup.find_all('div', attrs={'class': 'movietopmod'})
    print(list)
    movies = []
    for item in list:
        print(item)
        txtbox = item.find('div', attrs={'class': 'txtbox'})
        print(txtbox)
        name = txtbox.find('h3').a.get_text()
        totalnum = item.find('p', attrs={'class': 'totalnum'})
        type = totalnum.get_text()
        gradebox = item.find('div', attrs={'class': 'gradebox'})
        if gradebox.p:
            grade = gradebox.p.get_text()
        movie = {
            'name': name,
            'type': type,
            'price': grade
        }
        movies.append(movie)
    return render_template('movie.html', movies=movies)


if __name__ == '__main__':
    app.run(debug=True)
