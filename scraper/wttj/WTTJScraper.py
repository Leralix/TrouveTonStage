import random
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from .WTTJOfferScraper import WTTJOfferScraper

mainUrl = "https://www.welcometothejungle.com/fr/jobs?page=1&groupBy=job&sortBy=mostRelevant&query=&refinementList" \
          "%5Bcontract_type_names.fr%5D%5B%5D=Stage "


class WTTJScraper:

    def __init__(self, webdriver_path: str, nb_pages: int, output_name: str = None, min_delai: int = 5,
                 max_delai: int = 7, update_every: int = 0, url_csv=None):
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

        try:
            self.chrome = self.initialisation_(self.webdriver_path)

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

            self.df.to_csv(self.output_name, index=False)

        except:
            pass

    @staticmethod
    def initialisation_(webdriver_path):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        chrome = webdriver.Chrome(options=options, executable_path=webdriver_path)
        return chrome

    def offers_links_(self, nb_pages):
        url_list = []

        self.chrome.get(mainUrl)
        print("get_page")
        df_url = pd.DataFrame(columns=['url'])

        for i in range(1, nb_pages + 1):
            time.sleep(random.randrange(5, 7))
            try:
                test2 = self.chrome.find_elements("xpath", "//ol/div[contains(@class,'sc-cwSeag')]/li/article/div/a")
            except NoSuchElementException:
                break

            for url in test2:
                url_list.append(url.get_attribute("href"))
                dicti = {
                    "url": url.get_attribute("href")
                }

                df_url = pd.concat([df_url, pd.DataFrame(dicti.values(), columns=['url'])], ignore_index=True)
                print("df_url")
            # Changement de pages
            try:
                changer_page_supp = self.chrome.find_element("xpath",
                                                             "//ul/li/a[contains(@id,'-8')]")

            except NoSuchElementException:
                print("marche pas")
                break
            df_url.to_csv('./data/temp/temp_wttj_links.csv')
            changer_page_supp.click()

        return url_list

    def scrap_(self, links):
        count = 0
        print(len(links))
        for url in links:

            ws = WTTJOfferScraper(self.chrome, url)
            df_offer = ws.scrap_page()

            self.df = pd.concat([self.df, df_offer], ignore_index=True)

            count += 1
            print(count)
            if (self.update_every != 0) and (count % self.update_every == 0):
                self.df.to_csv('./data/temp/temp_wttj_offer.csv', index=False)

            time.sleep(random.randint(self.min_delai, self.max_delai))
