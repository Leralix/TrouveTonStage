from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import random


liens = pd.read_csv("4databaseWTTJ.csv")

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

chrome = webdriver.Chrome(options=options,executable_path='./chromedriver.exe')


df = pd.DataFrame(
    columns=["Titre", "Type de contrat", "Bac", "Durée", "Début", "Nom entreprise", "Localisation", "Description",
             'url'])
for row in liens.iterrows():

    # Connection a la page
    urlEmploi = row[1][1]
    chrome.get(urlEmploi)

    # Infos qui apparaissent à 100%
    NomEntreprise = chrome.find_element("xpath", "//div/div/div/a/h4").text
    NomEmploi = chrome.find_element("xpath", "//div/h1[contains(@class, 'sc-12bzhsi-3 jsHMkb')]").text
    print(NomEmploi)

    try:
        localisationEmploi = chrome.find_element("xpath",
                                                 "//div/ul/li/span[contains(@class, 'sc-16yjgsd-3 cToOtz')]/a/span").text
    except NoSuchElementException:
        localisationEmploi = "NA"
    try:
        TypeEmploiEtDuree = chrome.find_elements("xpath",
                                                 "//div/ul/li/span[contains(@class, 'sc-16yjgsd-3 bCCdzk')]/span")
    except NoSuchElementException:
        TypeEmploiEtDuree = ["NA", "NA"]
    try:
        TypeEmploi = TypeEmploiEtDuree[0].text
    except NoSuchElementException:
        TypeEmploi = "NA"

    try:
        DureeEmploi = TypeEmploiEtDuree[1].text
    except NoSuchElementException:
        DureeEmploi = "NA"

    try:
        NiveauEtude = chrome.find_elements("xpath", "//div/ul/li/span[contains(@class, 'sc-16yjgsd-3 eJxlVj')]/span")[
            1].text
    except NoSuchElementException:
        NiveauEtude = "NA"

    try:
        DebutEmploi = chrome.find_element("xpath",
                                          "//div/ul/li/span[contains(@class, 'sc-16yjgsd-3 bCCdzk')]/time/span").text
    except NoSuchElementException:
        DebutEmploi = "NA"

    descriptionEmploi = chrome.find_elements("xpath", "//div[contains(@class, 'itvpid-1 jpqriD')]")
    fulldesc2 = []
    for descPart in descriptionEmploi:
        fulldesc2.append(descPart.text)
    descriptionEmploiFinal = ''.join(fulldesc2)

    # Nettoyer certaines variables:

    DureeEmploi = DureeEmploi.replace('(', '').replace(')', '')
    # NiveauEtude = NiveauEtude.replace('(', '').replace(')', '')

    # Ajouts des infos au tableau existant
    df2 = pd.DataFrame([[NomEmploi, TypeEmploi, NiveauEtude, DureeEmploi, DebutEmploi, NomEntreprise,
                         localisationEmploi, descriptionEmploiFinal, urlEmploi]],
                       columns=["Titre", "Type de contrat", "Bac", "Durée", "Début", "Nom entreprise", "Localisation",
                                "Description", 'url'])
    df = pd.concat([df, df2])

    time.sleep(random.randrange(3, 4))


df.to_csv("DatabaseFInaleWTTJ.csv")