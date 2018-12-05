from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
import json
import urllib3

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


if __name__ == '__main__':
    app.run(debug=True)
