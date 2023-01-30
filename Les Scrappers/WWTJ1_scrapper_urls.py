import requests
from selenium import webdriver
import time
import pandas as pd
import random
from selenium.common.exceptions import NoSuchElementException


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

chrome = webdriver.Chrome(options=options,executable_path='./chromedriver.exe')

n = 50
mainUrl = "https://www.welcometothejungle.com/fr/jobs?page=1&groupBy=job&sortBy=mostRelevant&query=&refinementList%5Bcontract_type_names.fr%5D%5B%5D=Stage"


urlList = []
chrome.get(mainUrl)

for i in range(n):
    time.sleep(random.randrange(5,7))
    try:
        test2 = chrome.find_elements("xpath","//ol/div[contains(@class,'sc-cwSeag')]/li/article/div/a")
    except NoSuchElementException:
        break

    for url in test2:
        urlList.append(url.get_attribute("href"))
    time.sleep(1)
    try:
        changerPageSupp = chrome.find_element("xpath","//ul/li[contains(@class,'ais-Pagination-item ais-Pagination-item--nextPage')]")
    except NoSuchElementException:
        break
    changerPageSupp.click()

df = pd.DataFrame(urlList)
df.to_csv("4databaseWTTJ.csv")