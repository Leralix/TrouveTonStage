# This Python file uses the following encoding: utf-8
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests


from Indeed_Offer_new_regex import scrap_page

import time
import random

from webdriver_manager.chrome import ChromeDriverManager

# This is the main function
# Its role is to get a link on every job offer on a given page, then call the scraping function on each one.

# Configure the webdriver (Selenium), because Indeed in protected by Cloudflare, and simple scraper couldn't be used.
IS_LINUX = False
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
chrome = webdriver.Chrome(options=options,executable_path='./chromedriver.exe')

# Get the Indeed's main page, with one keyword: stage.
chrome.get("https://fr.indeed.com/jobs?q=stage")

# Accept the cookies after arriving on the page
# Wait until the button 'accept' is clickable.
wait = WebDriverWait(chrome, 15)
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
chrome.find_element('xpath','//*[@id="onetrust-accept-btn-handler"]').click()



# Function to scrap one job offer page (page containing multiple job offer)
# Parameters chrome (Webdriver used to perform the request), lien_page (link of the job offer page), df (dataframe where we want to add all the informations retrieved on the page)
def ScrapOnePage(chrome, lien_page, df):

    # The webdrive get to link passed in parameters
    chrome.get(lien_page)

    # Find all the links to each job offers
    cells = chrome.find_elements('xpath', '//ul[contains(@class,"jobsearch-ResultsList css-0")]//h2/a')

    # Retrieve all the href (link) and add those to a list
    href = []
    for elem in cells:
        href.append(elem.get_attribute("href"))

    # For each link found on the page
    # Get all the information from each links.
    for elem in href:

        # Get the webdrive on the page of the offers
        chrome.get(elem)

        # Scrap the page and get all the informations related to this offer
        list_content = scrap_page(chrome.page_source.encode('utf-8'))

        # Add to the dictionnary a url section
        list_content['url'] = elem

        # Append the dictionnary to the dataframe given in parameters
        df = df.append(pd.DataFrame(list_content))

        # Do a random pause to not flood the website and be spotted or banned.
        print("Pause")
        time.sleep(random.randint(6, 14))
        print("Fin Pause")

    # Return the dataframe containing all the informations off all jober offers contained on the link given in parameters.
    return df



# Main loop to scrap on all Indeed pages.
# Declare an empty dataframe that will contains our job offfers' informations;
df=pd.DataFrame()

# Because the first contains start=0 in its url, and the second one contains start=10 on its url.
# There is a 10 incrementation change on each url for the start field.
for i in range(0,40,10):
    # get the url correspondign to the page
    url = "https://fr.indeed.com/jobs?q=stage&start="+str(i)

    # Scrap this page
    # get all job offers contained, and get info from theses job offers.
    df = ScrapOnePage(chrome, url,df)


# Export the dataframe into a csv.
df_finale = df
df_finale.to_csv("testNEW3.csv",index=False)



