import os
import requests
from bs4 import BeautifulSoup
import shutil

res = requests.get("https://ibeauty01.com/%E9%83%AD%E9%9B%AA%E8%8A%99")

soup = BeautifulSoup(res.text,"html.parser")
l = soup.select('.image-item a')

if not os.path.exists('郭雪芙'):
    os.makedirs('郭雪芙')

for a in l:
    link = 'https://ibeauty01.com' + a['href']
    res2 = requests.get(link)
    soup2 = BeautifulSoup(res2.text, "html.parser")
    l2 = soup2.select('img')
    fname = '郭雪芙/' + l2[0]['src'].split('/')[-1]
    res2 = requests.get(l2[0]['src'], stream=True)
    f = open(fname, 'wb')
    shutil.copyfileobj(res2.raw, f)
    f.close()
    del res2

