from hashlib import md5
import pymongo
from urllib.parse import urlencode
from requests.exceptions import RequestException
import requests
import re
import json
from bs4 import BeautifulSoup
from config import *
import os
from multiprocessing import Pool

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

if not os.path.exists('街拍'):
	os.makedirs('街拍')

def get_one_index(offset, keyword):
	data = {
		'offset' : offset,
		'format' : 'json',
		'keyword' : keyword,
		'autoload' : 'true',
		'count' : '20',
		'cur_tab' : '1'
	}
	url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
	try:
		response = requests.get(url)
		if response.status_code == 200:
			return response.text
		return None
	except RequestException:
		#print('AJAX請求失敗', url)
		return None

def parse_page_index(html):
	if html != None:
		data = json.loads(html)
		if data and 'data' in data.keys():
			for item in data.get('data'):
				yield [item.get('media_name'), item.get('url')]

def get_page_detail(url):
	try:
		response = requests.get(url)
		if response.status_code == 200:
			return response.text
		return None
	except RequestException:
		#print('文章請求失敗', url)
		return None

def parse_page_detail(html, url):
	soup = BeautifulSoup(html, 'lxml')
	title = soup.select('title')[0].get_text()
	#print(title)
	images_pattern = re.compile('var gallery = (.*?);', re.S)
	result = re.search(images_pattern, html)
	if result:
		data = json.loads(result.group(1))		
		if data and 'sub_images' in data.keys():
			sub_images = data.get('sub_images')
			images = [item.get('url') for item in sub_images]
			for image in images:
				download_image(image)
			
			#return {
			#	'title' : title,
			#	'url' : url,
			#	'images' : images,
			#}

def save_to_mongo(result):
	if db[MONGO_TABLE].insert(result):
		#print('存儲到MongoDB成功')
		return True
	return False

def download_image(url):
	try:
		response = requests.get(url)
		if response.status_code == 200:
			save_image(response.content)
			print(url, '下載完成')
		return None
	except RequestException:
		print('請求圖片出錯', url)
		return None

def save_image(content):
	file_path = '{0}/{1}.{2}'.format('街拍', md5(content).hexdigest(), 'jpg')
	if not os.path.exists(file_path):
		with open(file_path, 'wb') as f:
			f.write(content)
			f.close()

def main(offset):
	html = get_one_index(offset, '街拍')
	for url in parse_page_index(html):
		#print(offset, url[0])
		html = get_page_detail(url[1])
		if html:
			result = parse_page_detail(html, url)
			#if result != None:
			#	save_to_mongo(result)

if __name__ == '__main__':
	for i in range(GROUP_START, GROUP_END+1):
		main(i*20)
	#groups = [x*20 for x in range(GROUP_START, GROUP_END+1)]
	#pool = Pool()
	#pool.map(main, groups)



