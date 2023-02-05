import pandas as pd
import time
from IndeedScraper import IndeedScraper
from WTTJScraper import WTTJScraper
from threading import Thread

from Data_Cleaner import DataCleaner

ISc = IndeedScraper(
    webdriver_path='./chromedriver.exe',
    nb_pages=1,
    output_name="INDEED.csv",
    min_delai=3,
    update_every=0
)

wts = WTTJScraper(
    webdriver_path='./chromedriver.exe',
    nb_pages=1,
    output_name="WTTJ.csv",
    update_every=0,
)


thread_list = []
thrd1 = Thread(target=ISc.launch_scraping)
thrd2 = Thread(target=wts.launch_scraping)
thread_list.append(thrd1)
thread_list.append(thrd2)

# Demarre le thread
for t in thread_list:
    t.start()

# Attend que chaque thread ait terminé
for t in thread_list:
    t.join()


# Délai pour attendre la création des csv.
time.sleep(3)

# Lecture et cleaning du fichier joignant les 2 csv.
df1 = pd.read_csv("INDEED.csv")
df2 = pd.read_csv("WTTJ.csv")
df3 = pd.concat([df1,df2],axis=0,ignore_index=True)
df3.to_csv('finale.csv',index=False)

DataCleaner('finale.csv','cleaned_data.csv')

