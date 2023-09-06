import json
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Movie:
    title: str
    launch_year: str
    url: str
    img: str
    rating: str
    genres: list[str] 
    popularity: str
    directors: list[str]

    def __init__(self, title, launch_year, url, img, rating):
        self.title = title
        self.launch_year = launch_year
        self.url = url
        self.img = img
        self.rating = rating
    
    def to_json(self):
        return {
            "title": self.title,
            "launch_year": self.launch_year,
            "url": self.url,
            "img": self.img,
            "rating": self.rating,
            "genres": self.genres,
            "popularity": self.popularity,
            "directors": self.directors
        }
        

driver = webdriver.Chrome()


driver.get("https://www.imdb.com/")
driver.maximize_window()

# ================== ETAPA 1==================

# Clicar no menu haburguer 
menu = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'imdbHeader-navDrawerOpen')))
menu.click()

# Clicar em Top 250
top_250_op = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="imdbHeader-navDrawer"]/div/div[2]/div/div[1]/span/div/div/ul/a[2]')))
top_250_op.click()

# Obter lista do top 250 filmes
ul_movie_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul')))
li_movie_list = ul_movie_list.find_elements(By.XPATH, './/li[contains(@class, "ipc-metadata-list-summary-item")]')

movie_list = []
index = 1

for movie in li_movie_list:

    # Movie Title
    title = movie.find_element(By.XPATH, f'//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul/li[{index}]/div[2]/div/div/div[1]/a/h3').text
    # Regex to remove the number and dot from the title
    title = re.sub(r'^.*?\.\s*', '', title)

    # Launch Year 
    launch_year = movie.find_element(By.XPATH, f'//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul/li[{index}]/div[2]/div/div/div[2]/span[1]').text
    
    # Poster URL
    url = movie.find_element(By.XPATH, f'//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul/li[{index}]/div[1]/div/a').get_attribute("href")

    # Poster Image
    img = movie.find_element(By.XPATH, f'//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul/li[{index}]/div[1]/div/div[2]/img').get_attribute("src")

    # IMDB Rating
    rating = movie.find_element(By.XPATH, f'//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul/li[{index}]/div[2]/div/div/span/div/span').text.split()[0]
    
    # Create Movie Object
    movie = Movie(title, launch_year, url, img, rating)
    movie_list.append(movie)

    index += 1


# ================== ETAPA 2 ==================

index = 1
for movie in movie_list:
    driver.get(movie.url)
    driver.maximize_window()

    # Movie genres list
    try:
        div_genre_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[1]/div[2]')))
        a_genre_list = div_genre_list.find_elements(By.TAG_NAME, 'a')
        genres = [genres.text for genres in a_genre_list]
    except:
        genres = []
    movie.genres = genres

    # Movie popularity
    try:
        popularity = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[3]/a/span/div/div[2]/div[1]'))).text 
    except:
        popularity = 0
    movie.popularity = popularity

    # Movie directors list (if doesn't have information, set as "unknown")
    try:
        ul_directors = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[1]/div/ul')))
        li_directors = ul_directors.find_elements(By.TAG_NAME, 'li')
        director_list = []
        for li in li_directors:
            a_director = li.find_element(By.TAG_NAME, 'a') 
            director_list.append(a_director.text)
    except:
        director_list = []
    movie.directors = director_list

    index += 1

# ================== ETAPA 3 ==================
movies_json = []
for movie in movie_list:
    movies_json.append(movie.to_json())
    
# Save in JSON file
with open('./result.json', 'w') as f:
    json.dump(movies_json, f)
    