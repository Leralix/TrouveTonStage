# This Python file uses the following encoding: utf-8
import random
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from .IndeedOfferScraper import IndeedOfferScraper


class IndeedScraper:

    def __init__(self, webdriver_path: str, nb_pages: int, output_name: str = None, min_delai: int = 6,
                 max_delai: int = 14, update_every: int = 0):
        self.chrome = None
        self.indeed_df = pd.DataFrame()

        self.webdriver_path = webdriver_path
        self.nb_pages = nb_pages
        self.update_every = update_every
        self.counter = 0
        self.output_name = output_name

        self.min_delai = min_delai
        self.max_delai = max_delai

    # This is the main function
    # Its role is to get a link on every job offer on a given page, then call the scraping function on each one.

    def launch_scraping(self):

        try:
            self.chrome = self.initialisation_(self.webdriver_path)
            self.scrap(self.nb_pages)

            if self.output_name is not None:
                self.to_csv(self.output_name)
        except:
            raise 'No Webdriver found'

    @staticmethod
    def initialisation_(webdriver_path):
        # Configure the webdriver (Selenium), because Indeed in protected by Cloudflare, and simple scraper couldn't
        # be used.
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        chrome = webdriver.Chrome(options=options, executable_path=webdriver_path)

        return chrome

    def accept_cookies_(self):

        # Accept the cookies after arriving on the page
        # Wait until the button 'accept' is clickable.
        wait = WebDriverWait(self.chrome, 15)
        wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
        self.chrome.find_element('xpath', '//*[@id="onetrust-accept-btn-handler"]').click()

    # Function to scrap one job offer page (page containing multiple job offer) Parameters chrome (Webdriver used to
    # perform the request), lien_page (link of the job offer page), df (dataframe where we want to add all the
    # informations retrieved on the page)
    def offers_link_(self, lien_page: str):

        # The webdrive get to link passed in parameters
        self.chrome.get(lien_page)

        # Find all the links to each job offers
        cells = self.chrome.find_elements('xpath', '//ul[contains(@class,"jobsearch-ResultsList css-0")]//h2/a')

        # Retrieve all the href (link) and add those to a list
        href = []
        for elem in cells:
            href.append(elem.get_attribute("href"))

        return href

    def scrap_offers_(self, url_list, df):

        # For each link found on the page
        # Get all the information from each links.

        for elem in url_list:

            # Get the webdrive on the page of the offers
            self.chrome.get(elem)

            # Scrap the page and get all the informations related to this offer
            list_content = IndeedOfferScraper(self.chrome.page_source.encode('utf-8')).scrap_page()

            # Add to the dictionnary a url section
            list_content['url'] = elem

            # Concatenate the dictionnary to the dataframe given in parameters
            df = pd.concat([df, pd.DataFrame(list_content)], ignore_index=True)

            self.counter += 1
            if (self.update_every != 0) and (self.counter % self.update_every == 0):
                df.to_csv("./data/temp/temp_indeed_offer.csv", index=False)

            # Do a random pause to not flood the website and be spotted or banned.
            time.sleep(random.randint(self.min_delai, self.max_delai))

        # Return the dataframe containing all the informations off all jober offers contained on the link given in
        # parameters.
        return df

    def scrap(self, nb_pages: int):
        # Get the Indeed's main page, with one keyword: stage.
        self.chrome.get("https://fr.indeed.com/jobs?q=stage")

        self.accept_cookies_()

        for i in range(0, nb_pages * 10, 10):
            # get the url correspondign to the page
            url = "https://fr.indeed.com/jobs?q=stage&start=" + str(i)

            offers_link = self.offers_link_(url)

            # Scrap this page
            # get all job offers contained, and get info from these job offers.
            self.indeed_df = self.scrap_offers_(offers_link, self.indeed_df)

    def to_csv(self, output_name):
        self.indeed_df.to_csv(output_name, index=False)
