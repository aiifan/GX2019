import json

import requests
from fake_useragent import UserAgent

url = "https://www.zhihu.com/signin?next=%2F"

headers = {
    "User-Agent": UserAgent().random
   }

r = requests.get(url, headers=headers)

print(r.headers)
print(r.text)
