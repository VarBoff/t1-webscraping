import re
import csv
from pprint import pprint
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup

url_paises = []

url = 'http://127.0.0.1:8000'
html = urlopen(url+'/places/default/index')
bs = BeautifulSoup(html, 'html.parser')


def get_next_button_link(bs):
	buttons = bs.find('div', {'id':'pagination'}).find_all('a')
	for button in buttons:
		if 'Next >' in list(button.children):
			return button.attrs['href']
	return None


next_page_href = get_next_button_link(bs)
while next_page_href is not None:
	for link in bs.find('div', {'id':'results'}).find_all(
		'a', href=re.compile('^(/places/)((?!:).)*$')):
		if 'href' in link.attrs:
			url_paises.append(link.attrs['href'])
	html = urlopen(url+next_page_href)
	bs = BeautifulSoup(html, 'html.parser')
	next_page_href = get_next_button_link(bs)
	

headers = ['country', 'capital', 'currency', 'population', 'timestamp']
paises = []

def get_field_with_id(bs, id):
	children = list(bs.find('tr', {'id': id}).find('td', {'class': 'w2p_fw'}).children)
	if len(children) > 0:
		return children[0]
	return None

for u in url_paises:
	html = urlopen(url+u)
	bs = BeautifulSoup(html, 'html.parser')

	country_field = get_field_with_id(bs, 'places_country__row')
	capital_field = get_field_with_id(bs, 'places_capital__row')
	currency_field = get_field_with_id(bs, 'places_currency_name__row')
	population_field = get_field_with_id(bs, 'places_population__row')
	time = datetime.now()
	paises.append([country_field, capital_field, currency_field, population_field, time])

with open('./tarefa1/paises.csv', 'w') as file:
	writer = csv.writer(file)
	writer.writerows(paises)