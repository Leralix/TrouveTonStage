import pandas as pd
import time
from indeed.IndeedScraper import IndeedScraper
from wttj.WTTJScraper import WTTJScraper
from threading import Thread
import os

from Data_Cleaner import DataCleaner

"""ISc = IndeedScraper(
    webdriver_path='./webdriver/chromedriver.exe',
    nb_pages=2,
    output_name="./data/INDEED.csv",
    min_delai=3,
    update_every=1
)"""

wts = WTTJScraper(
    webdriver_path='./webdriver/chromedriver.exe',
    nb_pages=2,
    output_name="./data/WTTJ.csv",
    url_csv='./data/temp/temp_wttj_links.csv',
    update_every=1,
)

thread_list = []
#thrd1 = Thread(target=ISc.launch_scraping)
thrd2 = Thread(target=wts.launch_scraping)
#thread_list.append(thrd1)
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
df1 = pd.read_csv("./data/INDEED.csv")
df2 = pd.read_csv("./data/WTTJ.csv")
df3 = pd.concat([df1, df2], axis=0, ignore_index=True)

if os.path.isfile('./data/Ind_Wttj.csv')==True :
    df4 = pd.read_csv('./data/Ind_Wttj.csv')
    df_final = pd.concat([df4,df3],axis=0,ignore_index=True)
    df_final.to_csv('./data/Ind_Wttj.csv',index=False)
else :
    df3.to_csv('./data/Ind_Wttj.csv', index=False)


# Clean csv and export the result
dc = DataCleaner('./data/Ind_Wttj.csv')
dc.clean('./clean_data/clean_data.csv')
