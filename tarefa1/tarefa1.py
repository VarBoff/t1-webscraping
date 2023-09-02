import re
import csv
from pprint import pprint
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = 'http://127.0.0.1:8000'


class HTMLDownloaderCrawler:

	@staticmethod
	def get_next_button_link(bs):
		buttons = bs.find('div', {'id':'pagination'}).find_all('a')
		for button in buttons:
			if 'Next >' in list(button.children):
				return button.attrs['href']
		return None

	@staticmethod
	def run(url):
		url_paises = []
		html = urlopen(url+'/places/default/index')
		bs = BeautifulSoup(html, 'html.parser')

		next_page_href = HTMLDownloaderCrawler.get_next_button_link(bs)
		while next_page_href is not None:
			for link in bs.find('div', {'id':'results'}).find_all(
				'a', href=re.compile('^(/places/)((?!:).)*$')):
				if 'href' in link.attrs:
					url_paises.append(link.attrs['href'])
			html = urlopen(url+next_page_href)
			bs = BeautifulSoup(html, 'html.parser')
			next_page_href = HTMLDownloaderCrawler.get_next_button_link(bs)
		return url_paises


class CountriesScrapper:
	
	@staticmethod
	def get_field_with_id(bs, id):
		children = list(bs.find('tr', {'id': id}).find('td', {'class': 'w2p_fw'}).children)
		if len(children) > 0:
			return children[0]
		return None

	@staticmethod
	def save_csv(lista):
		with open('./tarefa1/paises.csv', 'w') as file:
			writer = csv.writer(file)
			writer.writerows(lista)

	@staticmethod
	def run(url_paises):
		paises = []
		for u in url_paises:
			html = urlopen(url+u)
			bs = BeautifulSoup(html, 'html.parser')

			country_field = CountriesScrapper.get_field_with_id(bs, 'places_country__row')
			capital_field = CountriesScrapper.get_field_with_id(bs, 'places_capital__row')
			currency_field = CountriesScrapper.get_field_with_id(bs, 'places_currency_name__row')
			population_field = CountriesScrapper.get_field_with_id(bs, 'places_population__row')
			time = datetime.now()
			paises.append([country_field, capital_field, currency_field, population_field, time, u])

		CountriesScrapper.save_csv(paises)


class CountryMonitorCrawler:

	@staticmethod
	def read_csv(csv_filename):
		with open(csv_filename, 'r') as file:
			reader = csv.reader(file)
			return list(reader)
			
	@staticmethod
	def save_csv(lista, filename):
		with open(filename, 'w') as file:
			writer = csv.writer(file)
			writer.writerows(lista)
		
	@staticmethod
	def run(csv_filename):
		countries = CountryMonitorCrawler.read_csv(csv_filename)

		for country in countries:
			html = urlopen(url+country[5])
			bs = BeautifulSoup(html, 'html.parser')

			country_field = CountriesScrapper.get_field_with_id(bs, 'places_country__row')
			capital_field = CountriesScrapper.get_field_with_id(bs, 'places_capital__row')
			currency_field = CountriesScrapper.get_field_with_id(bs, 'places_currency_name__row')
			population_field = CountriesScrapper.get_field_with_id(bs, 'places_population__row')

			modified_flag = False
			if country_field != country[0]:
				country[0] = country_field
				modified_flag = True
			if capital_field != country[1]:
				country[1] = capital_field
				modified_flag = True
			if currency_field != country[2]:
				country[2] = currency_field
				modified_flag = True
			if population_field != country[3]:
				country[3] = population_field
				modified_flag = True

			if modified_flag:
				time = datetime.now()
				country[4] = time
		
		CountryMonitorCrawler.save_csv(countries, csv_filename)


# Tarefa 1
url_paises = HTMLDownloaderCrawler.run(url)

# Tarefa 2
CountriesScrapper.run(url_paises)

# Tarefa 3
CountryMonitorCrawler.run('./tarefa1/paises.csv')

print('\n\033[91m⠀⠀⠀⠀⠀⠀⠀⠀⣀⠤⠔⠒⣬⠉⠉⣍⡍⠁⢒⠢⠤⣀')
print('\033[91m⠀⠀⠀⠀⠀⡠⢔⢍⠀⠸⠤⣀⠡⢥⣤⣥⡥⠄⣁⡃⠠⠒⠉⠢⢄')
print('\033[91m⠀⠀⠀⡠⢊⣠⡀⢈⢤⣢⣵⣾⣿⠟⠛⠛⠟⢿⣿⣾⣵⡢⡀⠎⢀⣑⢄⠀⠀⠀')
print('\033[91m⠀⠀⡔⢅⡀⢁⢔⣵⣿⣿⣿⣿⠿⢶⠀⠀⢰⠳⢿⣿⣿⣿⣷⣕⡐⠘⠈⢢⠀⠀')
print('\033[91m⠀⡜⠀⠀⠠⣳⣿⣿⣿⣿⠏⠀⣠⣼⠀⠀⢸⣤⠀⠉⢻⣿⣿⣿⣮⢆⢺⠧⢣⠀')
print('\033[91m⢰⠙⠤⢢⣳⣿⣿⣿⣿⠟⠀⠀⣀⣀⠀⠀⢀⣀⠂⠠⠙⠁⢹⣿⣿⣯⠆⢄⢀⡆')
print('\033[91m⡆⠀⠀⡌⣿⣿⣿⠟⠁⢸⡀⠀⠈⢻⠀⠀⢸⣧⣀⣿⣶⣄⢸⣿⣿⣿⣼⠈⠁⢰')
print('\033[91m⡇⠚⠃⣿⣿⣟⠁⠀⠀⢾⣿⣦⣀⣸⠀⠀⢸⠉⠙⠻⣿⣿⣿⣿⣿⣿⣿⠘⠉⢸')
print('\033[91m⠇⠀⠀⢃⣿⣿⣷⣄⠀⠈⡟⠉⠙⣿⠀⠀⢸⣄⡀⠀⠈⠿⠻⣿⣿⣿⢻⠀⠀⢸')
print('\033[91m⠸⡀⠀⠘⡽⣿⣿⣿⡷⠜⠀⠀⡰⠛⠒⠒⠚⠛⢱⠀⠀⢸⣾⣿⣿⣟⠆⠀⠀⠇')
print('\033[91m⠀⢣⠀⠀⠘⡽⣿⣿⣦⣤⡀⠈⠓⠶⠒⠒⢲⠶⠋⠀⣠⣿⣿⣿⢟⠎⠀⠀⡜⠀')
print('\033[91m⠀⠀⠣⡀⠀⠈⠪⡻⣿⣿⣿⣷⣦⣤⠀⠀⢸⣤⣴⣾⣿⣿⣿⠋⠁⠀⢀⠜⠀⠀')
print('\033[91m⠀⠀⠀⠑⢄⠀⠀⠈⠚⠝⡻⢿⣿⣤⣤⣠⣤⣴⡿⢿⡻⠑⠁⠀⠀⡠⠊⠀⠀⠀')
print('\033[91m⠀⠀⠀⠀⠀⠑⠢⣀⠀⠀⠀⡍⠐⢚⡛⢛⣓⠂⡭⡄⠀⠀⣀⠔⠊⠀⠀⠀⠀⠀')
print('\033[91m⠀⠀⠀⠀⠀⠀⠀⠀⠉⠒⠨⠥⢀⣈⣃⣈⣚⣀⠤⠅⠒⠉⠀⠀⠀⠀⠀⠀⠀⠀')
