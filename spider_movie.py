import os
import codecs
import requests
from requests.exceptions import RequestException
import re
import csv

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
	pattern = re.compile('<div class="tr">.*?<div class="td">(.*?)</div>.*?<a href="(.*?)">.*?</a>.*?<div class="td starwithnum">', re.S)
	items = re.findall(pattern, html)
	
	with open('movie.csv','a', newline='' ,encoding='utf-8-sig') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['排名','電影','上映日期','片長','出品公司','觀眾評分'])

	for item in items:
		num, url = item
		url = url.split("\"")[0]
		
		html2 = get_one_page(url)
		id = url.split("id=")[1]
		review = 'https://tw.movies.yahoo.com/movieinfo_review.html/id=' + str(id)

		pattern2 = re.compile('<div class="movie_intro_info_r">.*?<h1>(.*?)</h1>.*?<h3>(.*?)</h3>.*?' + 
							'<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?' + 
							'<div class="score_num count" data-num="(.*?)">.*?</div>', re.S)
		infos = re.findall(pattern2, html2)
		for info in infos:
			head, head2, date, length, company, score = info
			date = date[5:]
			length =  length[5:]
			company = company[5:]
			l = [num, head, date, length, company, score]
			with open('movie.csv','a', newline='',encoding='utf-8-sig') as csvfile:
				writer = csv.writer(csvfile)
				writer.writerow(l)

def main():
	url = 'https://tw.movies.yahoo.com/chart.html'
	html = get_one_page(url)
	parse_one_page(html)

if __name__ == '__main__':
	main()


