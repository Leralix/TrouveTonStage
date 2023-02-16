# It scrapes the page of a job offer from Welcome To The Jungle and returns a dataframe with the information extracted
import numpy as np
import pandas as pd
from selenium.common.exceptions import NoSuchElementException


class WTTJOfferScraper:

    def __init__(self, chrome, url_offer):
        """
        The function __init__() is a constructor that initializes the class of WTTJOfferScraper.

        Args:
          chrome: The path to the webdriver executable.
          url_offer: The URL of the offer you want to scrape from Welcome To The Jungle.
        """
        self.chrome = chrome
        self.url_offer = url_offer

    def scrap_page(self):
        """
        It scrapes the page of a job offer from Welcom To The Jungle and returns a dataframe with the information extracted

        Returns:
          A dataframe with the information scraped from the job offer (url, location, degree, offer type, description, duration).
        """

        # Getting the url of the job offer and then get to the page
        url_emploi = self.url_offer
        self.chrome.get(url_emploi)

        # Getting the name of the company...
        nom_entreprise = self.chrome.find_element("xpath", "//div/div/div/a/h4").text
        # ...and the name of the job offer.
        nom_emploi = self.chrome.find_element("xpath", "//div/h1[contains(@class, 'sc-12bzhsi-3')]").text

        # Trying to find the location of the job offer. If it does not find it, it will return NA.
        try:
            localisation_emploi = self.chrome.find_element("xpath",
                                                           "//div/ul/li/span[contains(@class, 'sc-16yjgsd-3 "
                                                           "cToOtz')]/a/span").text
        except NoSuchElementException:
            localisation_emploi = "NA"

        # Trying to find the type of the job offer and the duration of the job offer. If it does not find it, it will
        # return NA.
        try:
            type_emploi_et_duree = self.chrome.find_elements("xpath",
                                                             "//div/ul/li/span[contains(@class, 'sc-16yjgsd-3 "
                                                             "bCCdzk')]/span")
        except NoSuchElementException:
            type_emploi_et_duree = [np.nan, np.nan]

        # Trying to find the type of the job offer. If it does not find it, it will return NA.
        try:
            type_emploi = type_emploi_et_duree[0].text
        except NoSuchElementException:
            type_emploi = np.nan

        # Trying to find the duration of the job offer. If it does not find it, it will return NA.
        try:
            if 'mois' in type_emploi_et_duree[1].text:
                duree_emploi = type_emploi_et_duree[1].text
            else:
                duree_emploi = np.nan
        except NoSuchElementException:
            duree_emploi = np.nan

        # Trying to find the degree of the job offer. If it does not find it, it will return NA.
        try:
            niveau_etude = \
                self.chrome.find_elements("xpath", "//div/ul/li/span[contains(@class, 'sc-16yjgsd-3 eJxlVj')]/span")[
                    1].text
        except NoSuchElementException:
            niveau_etude = np.nan

        # Trying to find the start date of the job offer. If it does not find it, it will return NA.
        try:
            debut_emploi = self.chrome.find_element("xpath",
                                                    "//div/ul/li/span[contains(@class, 'sc-16yjgsd-3 "
                                                    "bCCdzk')]/time/span").text
        except NoSuchElementException:
            debut_emploi = np.nan

        # Getting the description of the job offer.
        description_emploi = self.chrome.find_elements("xpath", "//div[contains(@class, 'itvpid-1')]")
        fulldesc2 = []
        for descPart in description_emploi:
            fulldesc2.append(descPart.text)
        description_emploi_final = ''.join(fulldesc2)


        # Trying to remove the parenthesis from the duration of the job offer. If it does not find it, it will return NA.
        try:
            duree_emploi = duree_emploi.replace('(', '').replace(')', '')
        except:
            pass

        # Creating a dataframe with the information scraped from the job offer.
        df = pd.DataFrame([[nom_emploi, type_emploi, niveau_etude, duree_emploi, debut_emploi, nom_entreprise,
                            localisation_emploi, description_emploi_final, url_emploi]],
                          columns=["Titre", "Type de contrat", "Bac", "Durée", "Début", "Nom entreprise",
                                   "Localisation",
                                   "Description", 'url'])

        return df
