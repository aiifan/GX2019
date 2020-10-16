import requests
import threading

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def download_page(url):

    headers = {"UserAgent":UserAgent().random}
    r = requests.get(url, headers=headers)
    return r.text


def get_content(html):
    
    soup = BeautifulSoup(html, "html.parser")
    con = soup.find(id="content")
    con_list = con.find_all("div",class_="article")
    return con_list

def down(i):
    content = i.find("div",class_='content').find("span").get_text()
    save_txt(content.strip("\n")+"\n")

def save_txt(*args):
    for i in args:
        with open("text.txt",'a', encoding="utf-8") as f:
            f.write(i)

if __name__ == "__main__":
    h = download_page("https://www.qiushibaike.com/text/")
    con_list = get_content(h)
    th = []
    for i in con_list:
        t = threading.Thread(target=down,args=(i,))
        th.append(t)
    for i in th:
        i.start()
        i.join()
