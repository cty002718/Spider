from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from config import *
import pymongo

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
browser.set_window_size(1400, 900)

wait = WebDriverWait(browser, 10)

def search():
    print('正在搜索')
    try:
        browser.get('https://www.taobao.com')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mq"))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
            '#J_PopSearch > div.sb-search > div > form > input[type="submit"]:nth-child(2)'))
        )
        input.send_keys('美食')
        submit.click()
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#J_relative > div.sort-row > div > div.pager > ul > li:nth-child(2)'))
        )
        return total.text
    except TimeoutException:
        return search()

def next_page(page_number):
    print('正在翻頁', page_number)
    try:
        next = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        '#J_relative > div.sort-row > div > div.pager > ul > li:nth-child(3) > a'))
        )
        next.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#J_relative > div.sort-row > div > div.pager > ul > li:nth-child(2) > span'),
                                              str(page_number))
        )
    except TimeoutException:
        return next_page(page_number)

def get_products():
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item'))
    )
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        #print(item.attr('data-index'))
        image = item.find('.pic .img').attr('src')
        if image == '//g.alicdn.com/s.gif':
            image = item.find('.pic .img').attr('data-ks-lazyload')

        product = {
            'image' : image,
            'price' : item.find('.price').text(),
            'deal' : item.find('.deal-cnt').text()[:-3],
            'title' : item.find('.title').text(),
            'shop' : item.find('.shop').text(),
            'location' : item.find('.location').text()
        }
        save_to_mongo(product)

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('儲存到MONGODB成功', result)
    except Exception:
        print('儲存到MONGODB失敗', result)


def main():
    try:
        total = search()
        total = int(total[2:])
        get_products()
        for i in range(2, total+1):
            next_page(i)
            get_products()
    except Exception:
        print('出錯啦')
    finally:
        browser.close()

if __name__ == '__main__':
    main()
