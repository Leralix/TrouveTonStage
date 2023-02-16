# It scrapes job offers from Indeed

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

    def __init__(self, webdriver_path: str, nb_pages: int, output_name: str = None, min_delai: int = 6,max_delai: int = 14, update_every: int = 0):
        """
        This function initializes the IndeedScraper class with the following parameters:

        - webdriver_path: the path to your webdriver executable file.
        - nb_pages:  the number of pages you want to scrape from Indeed
        - output_name: the name of the output file (like "test.csv")
        - min_delai: the minimum time to wait between two requests. Defaults to 6
        - max_delai: the maximum time to wait between two requests. Defaults to 14
        - update_every: the number of pages to scrape before updating a temporary csv file (in case of exception). Defaults to 0 (Never)

        Args:
          webdriver_path (str): the path to your webdriver executable file.
          nb_pages (int): the number of pages you want to scrape from Indeed
          output_name (str): the name of the output file (like "test.csv")
          min_delai (int): the minimum time to wait between two requests. Defaults to 6
          max_delai (int): the maximum time to wait between two requests. Defaults to 14
          update_every (int): the number of pages to scrape before updating a temporary csv file (in case of exception). Defaults to 0 (Never)
        """
        self.chrome = None
        self.indeed_df = pd.DataFrame()

        self.webdriver_path = webdriver_path
        self.nb_pages = nb_pages
        self.update_every = update_every
        self.counter = 0
        self.output_name = output_name

        self.min_delai = min_delai
        self.max_delai = max_delai

    def launch_scraping(self):
        """
        Execute the scraping process. It first initialises the webdriver, then if a url_csv was mentionned, take this file and scrap the url, otherwise it gathers all the url by going from page to page until the number of pages is reached.
        """

        # Trying to initialise the webdriver, scrap the pages and save the data to a csv file. If it fails, it raises an
        # error.
        try:
            self.chrome = self.initialisation_(self.webdriver_path)
            self.scrap(self.nb_pages)

            if self.output_name is not None:
                self.to_csv(self.output_name)
        except:
            raise 'No Webdriver found'

    @staticmethod
    def initialisation_(webdriver_path):
        """
        It initialises a webdriver with the given path, and returns the webdriver

        Args:
            webdriver_path: The path to the webdriver executable file you want to use.
        Returns:
            the webdriver initialised with the executable..
        """
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        chrome = webdriver.Chrome(options=options, executable_path=webdriver_path)

        return chrome

    def accept_cookies_(self):
        """
        It waits until the element with the id "onetrust-accept-btn-handler" is clickable, then clicks it
        """

        wait = WebDriverWait(self.chrome, 15)
        wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
        self.chrome.find_element('xpath', '//*[@id="onetrust-accept-btn-handler"]').click()


    def offers_link_(self, lien_page: str):
        """
        It takes a link as a parameter, goes to that link, finds all the links to each job offers, retrieves all the href
        (link) and add those to a list

        Args:
          lien_page (str): the link to the page where the job offers are

        Returns:
          A list of all the links to each job offers
        """

        # The webdriver get to link passed in parameters
        self.chrome.get(lien_page)

        # Find all the links to each job offers
        cells = self.chrome.find_elements('xpath', '//ul[contains(@class,"jobsearch-ResultsList css-0")]//h2/a')

        # Retrieve all the href (link) and add those to a list
        href = []
        for elem in cells:
            href.append(elem.get_attribute("href"))

        return href

    def scrap_offers_(self, url_list, df):
        """
        It scrapes the job offers from the list of urls given in parameters

        Args:
          url_list: a list of urls to scrap
          df: the dataframe that will contain all the informations of the offers.

        Returns:
          A dataframe containing all the informations off all jober offers contained on the link given in parameters.
        """

        # Go through all the job offer's url and scrap every one of them.
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
        """
        We get the main page of Indeed, we accept the cookies, and get the url of the page we want to scrap, we get the
        link of all the job offers contained in this page, and we scrap these job offers. Then do the same for the next pages

        Args:
          nb_pages (int): the number of pages you want to scrap.
        """

        # Get the Indeed's main page, with one keyword: stage.
        self.chrome.get("https://fr.indeed.com/jobs?q=stage")

        # Accept the cookies on the first entrance on the website
        self.accept_cookies_()

        for i in range(0, nb_pages * 10, 10):
            # get the url corresponding to the page
            url = "https://fr.indeed.com/jobs?q=stage&start=" + str(i)

            # Get every job offer links on the webpage.
            offers_link = self.offers_link_(url)

            # Scrap this page
            # get all job offers contained, and get info from these job offers.
            self.indeed_df = self.scrap_offers_(offers_link, self.indeed_df)

    def to_csv(self, output_name):
        """
        This function takes in a dataframe and an output name, and then exports the dataframe to a csv file with the given
        output name.

        Args:
          output_name: the name of the csv file you want to save the data to
        """
        self.indeed_df.to_csv(output_name, index=False)
