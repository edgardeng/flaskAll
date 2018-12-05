# Flask Crawl

> 

## Task

### 1. get data from remote api

get shanghai weather from [page_url](http://www.weather.com.cn/weather/101020100.shtml) and [api_url](http://www.weather.com.cn/data/sk/101020100.html)



### 2. get resource from remote website


### 3. get content from remote website and save in db

## Tech

### Urllib3

通过urllib3的request获取url结果
```python
@app.route('/weather')
def weather():
    api_url = 'http://www.weather.com.cn/data/sk/101020100.html'
    http = urllib3.PoolManager()
    r = http.request('GET', api_url)
    data = r.data.decode() 
    return data
```

### BeautifulSoap


### Crawpy

