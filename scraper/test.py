from selenium import webdriver

url ="https://www.welcometothejungle.com/fr/companies/galadrim/jobs/stage-de-fin-d-etudes-coach-produit_paris?q=6c088d4cb4c44b5ed81c96f5eab25932&o=410316"


from wttj import WTTJOfferScraper

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
chrome = webdriver.Chrome(options=options, executable_path='./webdriver/chromedriver.exe')


WTTJOfferScraper.WTTJOfferScraper(chrome,url).scrap_page()
