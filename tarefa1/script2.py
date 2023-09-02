from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.imdb.com/")
driver.maximize_window()

# Clicar no menu haburguer 
menu = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'imdbHeader-navDrawerOpen')))
menu.click()

# Clicar em Top 250
top_250_op = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="imdbHeader-navDrawer"]/div/div[2]/div/div[1]/span/div/div/ul/a[2]')))
top_250_op.click()

# Obter lista do top 250 filmes
ul_movie_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul')))
movie_list = ul_movie_list.find_elements(By.XPATH, './/li[contains(@class, "ipc-metadata-list-summary-item")]')

index = 1
for movie in movie_list:
    # começa quebrar aqui
	img = movie.find_element(By.XPATH, f'//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul/li[{index}]/div[1]/div/div[2]/img')
	print(img)

	url = movie.find_element(By.XPATH, './/a[contains(@class, "ipc-title-link-wrapper")]').get_attribute("href")
	print(url)
	title = movie.find_element(By.TAG_NAME, 'h3').text
	print(title)
    #launch_year = movie.find_element()
	index += 1
    

input()
