from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import random
import numpy as np


class WTTJOfferScraper:

    def __init__(self,chrome,url_offer):
        self.chrome = chrome
        self.url_offer = url_offer


    def scrap_page(self):
        # Connection a la page

        urlEmploi = self.url_offer
        self.chrome.get(urlEmploi)

        # Infos qui apparaissent à 100%
        NomEntreprise = self.chrome.find_element("xpath", "//div/div/div/a/h4").text
        NomEmploi = self.chrome.find_element("xpath", "//div/h1[contains(@class, 'sc-12bzhsi-3')]").text
        print(NomEmploi)

        try:
            localisationEmploi = self.chrome.find_element("xpath",
                                                     "//div/ul/li/span[contains(@class, 'sc-16yjgsd-3 cToOtz')]/a/span").text
        except NoSuchElementException:
            localisationEmploi = "NA"
        try:
            TypeEmploiEtDuree = self.chrome.find_elements("xpath",
                                                     "//div/ul/li/span[contains(@class, 'sc-16yjgsd-3 bCCdzk')]/span")
        except NoSuchElementException:
            TypeEmploiEtDuree = [np.nan, np.nan]
        try:
            TypeEmploi = TypeEmploiEtDuree[0].text
        except NoSuchElementException:
            TypeEmploi = np.nan

        try:
            DureeEmploi = TypeEmploiEtDuree[1].text
        except NoSuchElementException:
            DureeEmploi = np.nan

        try:
            NiveauEtude = self.chrome.find_elements("xpath", "//div/ul/li/span[contains(@class, 'sc-16yjgsd-3 eJxlVj')]/span")[
                1].text
        except NoSuchElementException:
            NiveauEtude = np.nan

        try:
            DebutEmploi = self.chrome.find_element("xpath",
                                              "//div/ul/li/span[contains(@class, 'sc-16yjgsd-3 bCCdzk')]/time/span").text
        except NoSuchElementException:
            DebutEmploi = np.nan

        descriptionEmploi = self.chrome.find_elements("xpath", "//div[contains(@class, 'itvpid-1')]")
        fulldesc2 = []
        for descPart in descriptionEmploi:
            fulldesc2.append(descPart.text)
        descriptionEmploiFinal = ''.join(fulldesc2)

        # Nettoyer certaines variables:

        DureeEmploi = DureeEmploi.replace('(', '').replace(')', '')
        # NiveauEtude = NiveauEtude.replace('(', '').replace(')', '')

        # Ajouts des infos au tableau existant
        df = pd.DataFrame([[NomEmploi, TypeEmploi, NiveauEtude, DureeEmploi, DebutEmploi, NomEntreprise,
                             localisationEmploi, descriptionEmploiFinal, urlEmploi]],
                           columns=["Titre", "Type de contrat", "Bac", "Durée", "Début", "Nom entreprise", "Localisation",
                                    "Description", 'url'])



        return df