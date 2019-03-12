import requests
from bs4 import BeautifulSoup 
import csv
from datetime import datetime
from multiprocessing import Pool


def get_html(url):
	r = requests.get(url)
	return r.text


def get_all_links(html):
	soup = BeautifulSoup(html, 'lxml')
	tds = soup.find('table', id='currencies').find_all('td', class_='currency-name')

	links = []
	for td in tds:
		a = td.find('a').get('href')
		link = 'https://coinmarketcap.com/' + a     	# link single current pages
		links.append(link)

	return links 										# return urls

def get_page_data(html):
	soup = BeautifulSoup(html, 'lxml')
	try:
		name = soup.find('h1', class_='details-panel-item--name').text.strip()
	except:
		name = 'name false'

	try:
		price = soup.find('span', id='quote_price').text.strip()
	except:
		price = "price false"

	data = {'name':name,
			'price':price}
	return data


def write_csv(data):
	'''this funck for using in make_all()'''

	with open('coinmarketcap.csv', 'a') as f:
		writer = csv.writer(f)
		writer.writerow( (data['name'], data['price']) )

		print(data['name'] + 'parsed  and price : ' + data['price'])


def make_all(url):
	'''this funck for using in main()'''

	html = get_html(url)
	data = get_page_data(html)
	write_csv(data)

def run_multiprocessing():
	
	url = 'https://coinmarketcap.com/'
	all_links = get_all_links(get_html(url))
	with Pool(20) as p :
		p.map(make_all, all_links)


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
	#run_multiprocessing()
	main()
