# Flask Crawl

> Use Urllib3, Scrapy, BeautifulSoup to crawl data


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

使用爬虫框架
### Scrapy

安装`pip install scrapy`

#### Scrapy的选择器XPath 和 Css

> 通过选择器表达式，选择Html文件中某个部分

Xpath可在XML文档中对元素和属性进行遍历。[教程](http://www.w3school.com.cn/xpath/index.asp)

常用的路径表达式 （选取节点）
* nodeName 选取此节点的所有子节点
* /         从跟节点选取
* //        从匹配选择的当前节点选择文档中的节点
* .         选取当前节点
* ..        选取父节点
* @         选取属性
* \*        匹配任何元素节点
* @*        匹配任何属性节点
* Node      匹配任何类型的节点

```python
from scrapt.selector import Selector
with open('./hero.xml', 'r') as fp:
    body = fp.read();
Selector(text=body).xpath('/*').extract()
```

Css常用的选择器

|类|示例|作用|
|:----|:----|:----|
| .class| .intro | 选择class="intro"的所有元素|
|#.id| #name|选择id="name"的所有元素|
|* | *| 选择所有元素|
|element|p|选择所有<p>元素|
|element,element|div,p | 选择所有div元素和p元素|
|element element|div p | 选择div元素内部的所有p元素|
|[attribute]|[target]|选择所有带有target属性的元素|
|[attribute=value]|[target=_blank]|选择target=_blank的所有元素|

```python
Selector(text=body).css('class').extract()
Selector(text=body).css('class name').extract()

```

re选择器，通过正则表达式来提取数据

```python

Selector(text=body).xpath('class').re('>*<')
```
re方法返回unicode字符串的列表，所有无法构造嵌套

### 命令

`scrapy startproject project_name` 初始化一个scrapy项目
`scrapy genspider example example.com` 生成一个爬虫脚本example
`scrapy crawl example` 运行爬虫

### Crapy 项目的文件
```text
 |- mtime // 项目包
    |- spiders          // 爬虫文件
        |- _init_.py
        |- movie.py     //  爬虫处理文件
    |- __init__.py
    |- items.py         // 定义爬虫需要的项
    |- middlewares.py
    |- pipelines.py
    |- settings.py      // 设置文件
 |- scrapy.cfg // 配置文件       
```


### BeautifulSoup

安装`pip install beautifulsoup4`

#### BS解析器

* python标准库 BeautifulSoup(data, 'html.parser')

* lxml Html解析器 BeautifulSoup(data, 'lxml')

* Lxml Xml解析器 BeautifulSoup(data, 'xml')

* html5lib Xml 解析器 BeautifulSoup(data, 'html5lib')

安装lxml解析器 `pip install lxml`

#### bs4过滤器

```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(open('a.html'),'lxml')
soup.prettify

soup.ul
tag = soup.find('ul')
soup.find_all('ul')
soup.find('li', attrs={'nu':'3'})
tag.get('nu')
tag.a.get_text()
```
