import requests
import chardet
from lxml import html
URL = 'https://movie.douban.com/top250'
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"}
req = requests.get(URL, headers=header)
tree = html.fromstring(req.text)
movie_top = tree.xpath('//*[@id="content"]/div/div/ol/li/div/div/em/text()')
movie_name = tree.xpath('//*[@id="content"]/div/div/ol/li/div/div/div/a/span[1]/text()')
movie_img_url = tree.xpath('//*[@id="content"]/div/div/ol/li/div/div/a/img/@src')
img_html = requests.get(movie_img_url[1])

for top in movie_top:
    for name in movie_name:
        for movie_img in movie_img_url:
            
