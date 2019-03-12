import requests
from bs4 import BeautifulSoup 

def get_html(url):
	r = requests.get(url)
	return r.text


def get_all_links(html):
	soup = BeautifulSoup(html,'lxml')
	tds = soup.find('table', id='currencies').find_all('td', class_='currency-name')
	links = []
	for td in tds:
		a = td.find('a').get('href')
		links.append(a)
	return links

def main():
	url = 'https://coinmarketcap.com/'
	all_links = get_all_links(get_html(url))

	for i in all_links:
		print(i)

if __name__ == '__main__':
	main()