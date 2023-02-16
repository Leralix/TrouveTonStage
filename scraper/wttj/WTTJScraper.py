# It scrapes job offers from Welcome To The Jungle
import random
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from .WTTJOfferScraper import WTTJOfferScraper

mainUrl = "https://www.welcometothejungle.com/fr/jobs?page=1&groupBy=job&sortBy=mostRelevant&query=&refinementList" \
          "%5Bcontract_type_names.fr%5D%5B%5D=Stage "


class WTTJScraper:

    def __init__(self, webdriver_path: str, nb_pages: int, output_name: str = None, min_delai: int = 5,max_delai: int = 7, update_every: int = 0, url_csv=None):
        """
        The function __init__() is a constructor that initializes the class of WTTJScraper

        Args:
          webdriver_path (str): the path to your webdriver executable file.
          nb_pages (int): the number of pages you want to scrape from Welcome To The Jungle
          output_name (str): the name of the output file (like "test.csv")
          min_delai (int): the minimum time to wait between two requests. Defaults to 5
          max_delai (int): the maximum time to wait between two requests. Defaults to 7
          update_every (int): the number of pages to scrape before updating a temporary csv file (in case of exception). Defaults to 0 (Never)
          url_csv: the path to the csv file containing the urls to scrape (Welcome To The Jungle links). Defaults to None
        """
        self.chrome = None
        self.min_delai = min_delai
        self.max_delai = max_delai

        self.nb_pages = nb_pages
        self.output_name = output_name

        self.url_csv = url_csv

        self.webdriver_path = webdriver_path

        self.update_every = update_every

        self.df = pd.DataFrame()

    def launch_scraping(self):
        """
        Execute the scraping process. It first initialises the webdriver, then if a url_csv was mentionned, take this file and scrap the url, otherwise it gathers all the url by going from page to page until the number of pages is reached.
        """

        # Trying to launch the scraping process
        # If it does not work, pass it
        try:
            # Initializing the webdriver with the given path.
            self.chrome = self.initialisation_(self.webdriver_path)

            # Checking if the url_csv is not None, if it is not None, it will read the csv file and scrap the url,
            # otherwise it will gather all the url by going from page to page until the number of pages is reached.
            if self.url_csv is not None:
                url_list1 = pd.read_csv(self.url_csv)['url']
                self.scrap_(url_list1)
                print("FIN")
            else:
                print("url_list")
                url_list = self.offers_links_(self.nb_pages)
                print(len(url_list))
                self.scrap_(url_list)
                print("FIN")

            # Export the datafram with all the informations from the job offers scraped.
            self.df.to_csv(self.output_name, index=False)

        except:
            pass

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

    def offers_links_(self, nb_pages):
        """
        It scrapes the links of the offers from the first page of the website, then it clicks on the next page button and
        scrapes the links of the offers from the second page, and so on...

        Args:
          nb_pages: the number of pages you want to scrape from Welcome To The Jungle

        Returns:
          A list of job offers urls
        """

        url_list = []

        # Getting the main url of the website
        self.chrome.get(mainUrl)
        # and creating a dataframe with the column 'url'
        df_url = pd.DataFrame(columns=['url'])

        # Scraping the links of the offers from the first page of the website until we reach the number of pages given.
        for i in range(1, nb_pages + 1):

            # Wait a random delay
            time.sleep(random.randrange(5, 7))

            # Trying to find the main content of the page (it contains all the job offers)
            try:
                test2 = self.chrome.find_elements("xpath", "//ol/div[contains(@class,'sc-cwSeag')]/li/article/div/a")
            except NoSuchElementException:
                break

            # Appending the url of the job offers to a list and to a dataframe (in case of error).
            for url in test2:
                url_list.append(url.get_attribute("href"))
                dicti = {
                    "url": url.get_attribute("href")
                }

                df_url = pd.concat([df_url, pd.DataFrame(dicti.values(), columns=['url'])], ignore_index=True)

            # Trying to find the next page button, if it does not find it, it breaks the loop.
            try:
                changer_page_supp = self.chrome.find_element("xpath",
                                                             "//ul/li/a[contains(@id,'-8')]")

            except NoSuchElementException:
                print("marche pas")
                break

            # Export all the links scraped to have a backup
            # And click on the next page if the link exists.
            df_url.to_csv('./data/temp/temp_wttj_links.csv')
            changer_page_supp.click()

        return url_list

    def scrap_(self, links):
        """
        It scrapes the job offers contained in the list of links (links of job offers), and updates the dataframe if 'update_every' is different than 0.

        Args:
          links: list of links to scrap (basically job offers urls)
        """
        count = 0

        # Scraping the job offers contained in the list of links (links of job offers), and updates the dataframe if
        # 'update_every' is different than 0.
        for url in links:

            # Creating a new instance of the class WTTJOfferScraper, and then it is calling the function scrap_page() from
            # this instance to gather all the informations from the offer.
            ws = WTTJOfferScraper(self.chrome, url)
            df_offer = ws.scrap_page()

            # Concatenating the dataframe of the offer to the dataframe of the scraper.
            self.df = pd.concat([self.df, df_offer], ignore_index=True)


            # Updating the csv file every 'update_every' if different from 0.
            count += 1
            print(count)
            if (self.update_every != 0) and (count % self.update_every == 0):
                self.df.to_csv('./data/temp/temp_wttj_offer.csv', index=False)

            # Wait a random delay before scraping the next job offer.
            time.sleep(random.randint(self.min_delai, self.max_delai))
