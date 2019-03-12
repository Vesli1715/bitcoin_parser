import requests
from bs4 import BeautifulSoup 
import csv

from datetime import datetime

def get_html(url):
	r = requests.get(url)
	return r.text


def get_all_links(html):
	soup = BeautifulSoup(html,'lxml')
	tds = soup.find('table', id='currencies').find_all('td', class_='currency-name')
	links = []

	for td in tds:
		a = td.find('a').get('href')
		link = 'https://coinmarketcap.com/' + a
		links.append(link)

	return links

def get_page_data(html):
	soup =BeautifulSoup(html,'lxml')
	try:
		name = soup.find('h1', class_='details-panel-item--name').text.strip()
	except:
		name = 'name false'

	try:
		price = soup.find('spam', id='quote_price').text.strip()
	except:
		price = "price false"

	data = {'name':name,
			'price':price}
	return data

def write_csv(data):
	with open('coinmarketcap.csv', 'a') as f:
		writer = csv.writer(f)

		writer.writerow( (data['name'], data['price']) )

		print(data['name'], 'parsed')


def main():
	start = datetime.now()

	url = 'https://coinmarketcap.com/'
	all_links = get_all_links(get_html(url))

	for index, url in enumerate(all_links):

		html = get_html(url)
		data = get_page_data(html)
		write_csv(data)
		print(index)
	
	end = datetime.now()
	total = end - start
	print(total)


if __name__ == '__main__':
	main()