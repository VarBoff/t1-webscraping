from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.imdb.com/")
menu = driver.find_element(By.ID, "imdbHeader-navDrawerOpen")
menu.send_keys(Keys.RETURN)

menu_links = [link.get_attribute("href") for link in driver.find_elements(By.TAG_NAME, "a")]
driver.get(menu_links[2])

#print(f"{menu_links}\n")

input()
