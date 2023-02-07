import numpy as np
import pandas as pd
from selenium.common.exceptions import NoSuchElementException


class WTTJOfferScraper:

    def __init__(self, chrome, url_offer):
        self.chrome = chrome
        self.url_offer = url_offer

    def scrap_page(self):
        # Connection a la page

        url_emploi = self.url_offer
        self.chrome.get(url_emploi)

        # Infos qui apparaissent à 100%
        nom_entreprise = self.chrome.find_element("xpath", "//div/div/div/a/h4").text
        nom_emploi = self.chrome.find_element("xpath", "//div/h1[contains(@class, 'sc-12bzhsi-3')]").text
        print(nom_emploi)

        try:
            localisation_emploi = self.chrome.find_element("xpath",
                                                           "//div/ul/li/span[contains(@class, 'sc-16yjgsd-3 "
                                                           "cToOtz')]/a/span").text
        except NoSuchElementException:
            localisation_emploi = "NA"
        try:
            type_emploi_et_duree = self.chrome.find_elements("xpath",
                                                             "//div/ul/li/span[contains(@class, 'sc-16yjgsd-3 "
                                                             "bCCdzk')]/span")
        except NoSuchElementException:
            type_emploi_et_duree = [np.nan, np.nan]
        try:
            type_emploi = type_emploi_et_duree[0].text
        except NoSuchElementException:
            type_emploi = np.nan

        try:
            duree_emploi = type_emploi_et_duree[1].text
        except NoSuchElementException:
            duree_emploi = np.nan

        try:
            niveau_etude = \
                self.chrome.find_elements("xpath", "//div/ul/li/span[contains(@class, 'sc-16yjgsd-3 eJxlVj')]/span")[
                    1].text
        except NoSuchElementException:
            niveau_etude = np.nan

        try:
            debut_emploi = self.chrome.find_element("xpath",
                                                    "//div/ul/li/span[contains(@class, 'sc-16yjgsd-3 "
                                                    "bCCdzk')]/time/span").text
        except NoSuchElementException:
            debut_emploi = np.nan

        description_emploi = self.chrome.find_elements("xpath", "//div[contains(@class, 'itvpid-1')]")
        fulldesc2 = []
        for descPart in description_emploi:
            fulldesc2.append(descPart.text)
        description_emploi_final = ''.join(fulldesc2)

        # Nettoyer certaines variables:

        duree_emploi = duree_emploi.replace('(', '').replace(')', '')
        # NiveauEtude = NiveauEtude.replace('(', '').replace(')', '')

        # Ajouts des infos au tableau existant
        df = pd.DataFrame([[nom_emploi, type_emploi, niveau_etude, duree_emploi, debut_emploi, nom_entreprise,
                            localisation_emploi, description_emploi_final, url_emploi]],
                          columns=["Titre", "Type de contrat", "Bac", "Durée", "Début", "Nom entreprise",
                                   "Localisation",
                                   "Description", 'url'])

        return df
