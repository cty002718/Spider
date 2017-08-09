import os
from selenium import webdriver
import time
import requests

browser = webdriver.Chrome()
browser.get('https://acg.gamer.com.tw/billboard.php?p=ANIME&t=3&period=halfyear')

browser.find_element_by_link_text("清單").click()

link = browser.find_elements_by_css_selector(".ACG-tb1left a")

if not os.path.exists('動畫'):
	os.makedirs('動畫')

count = 0
for item in link:
	count += 1
#	if count > 10:
#		break
	url = item.get_attribute('href')
	browser.execute_script('window.open()')
	browser.switch_to_window(browser.window_handles[1])
	browser.get(url)
	head = browser.find_element_by_css_selector("h1").text
	head = str(count) + ' ' + head
	items1 = browser.find_elements_by_css_selector(".ACG-box1listA li")
	items2 = browser.find_elements_by_css_selector(".ACG-box1listB li")
	
	if not os.path.exists('動畫/' + head):
		os.makedirs('動畫/' + head)
	with open('動畫/' + head + '/作品簡介.txt', 'w') as f:
		f.write('作品名稱：' + head.split(" ")[1] + '\n')
		for item in items1 + items2:
			f.write(item.text + '\n')

	browser.find_elements_by_css_selector(".BH-slave_more button")[1].click()
	browser.find_element_by_link_text("圖片").click()
	pictures = browser.find_elements_by_class_name("bhib_image")
	for picture in pictures:
		url = picture.get_attribute('src')
		response = requests.get(url)
		with open('動畫/' + head + '/' + url.split("/")[-1], "wb") as f:
			f.write(response.content)
			f.close()

	browser.close()
	browser.switch_to_window(browser.window_handles[0])

browser.close()


