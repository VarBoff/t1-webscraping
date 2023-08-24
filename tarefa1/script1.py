import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

paises = []

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
			paises.append(link.attrs['href'])
	html = urlopen(url+next_page_href)
	bs = BeautifulSoup(html, 'html.parser')
	next_page_href = get_next_button_link(bs)
	
        
print(paises)