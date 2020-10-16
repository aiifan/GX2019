import requests
import threading
from lxml import html
import sqlite3

 # 获取10个页面的url
def get_top250_url():
    req = requests.get(URL, headers=header)
    tree = html.fromstring(req.text)
    links = [URL]
    link_a = tree.xpath('//*[@id="content"]/div/div[1]/div[2]/a/@href')
    for i in link_a:
        link = URL + i
        links.append(link)
    return links

def crawl_from_local(urls):
    movie_dict = {}
    movie_names = []
    movie_img_urls = []
    for url in urls:
        r = requests.get(url, headers=header)
        text = r.content.decode('utf-8')
        html = etree.HTML(text)
        movie_top = html.xpath('//*[@id="content"]/div/div/ol/li/div/div/em/text()')
        movie_name = html.xpath('//*[@id="content"]/div/div/ol/li/div/div/div/a/span[1]/text()')
        movie_img_url = html.xpath('//*[@id="content"]/div/div/ol/li/div/div/a/img/@src')
    return movie_names, movie_img_urls

def praat_picture_prefs(name, img_url):

    return None

if __name__ == "__main__":
    URL = 'https://movie.douban.com/top250'
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}
    # print(len(get_top250_url()))
    create_data()
    # movie_names = []
    # movie_img_urls = []
    # for url in get_top250_url():
    #     he = requests.get(url,headers=header)
    #     tree = html.fromstring(he.text)
    #     movie_top = html.xpath('//*[@id="content"]/div/div/ol/li/div/div/em/text()')
    #     movie_name = html.xpath('//*[@id="content"]/div/div/ol/li/div/div/div/a/span[1]/text()')
    #     movie_img_url = html.xpath('//*[@id="content"]/div/div/ol/li/div/div/a/img/@src')


