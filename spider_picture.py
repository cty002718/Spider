import os
import requests
from requests.exceptions import RequestException
import re

def get_one_page(url):
	try:
		response = requests.get(url)
		response.encoding = 'utf-8'
		if response.status_code == 200:
			return response.text
		return None
	except RequestException:
		return None

def parse_one_page(html):
	count = 0
	pattern = re.compile('<p class="text-center">▼(.*?)。</p>.*?<img class="center-block img-responsive img-rounded lazyload" data-src="(.*?)"/></p>', re.S)
	items = re.findall(pattern, html)
	for item in items:
		name, url = item
		count += 1
		name = str(count) + ' ' + name
		url = 'http://www.bomb01.com' + url
		picture = requests.get(url)
		with open('picture/' + name + '.jpg', 'wb') as f:
			f.write(picture.content)
			f.close()

def main():
	if not os.path.exists('picture'):
		os.makedirs('picture')

	url = 'http://www.bomb01.com/article/20663'
	html = get_one_page(url)
	parse_one_page(html)

if __name__ == '__main__':
	main()


