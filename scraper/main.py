# The main file that is used to launch the scraping and the cleaning of the data.
import pandas as pd
import time
from indeed.IndeedScraper import IndeedScraper
from wttj.WTTJScraper import WTTJScraper
from threading import Thread
import os
from Data_Cleaner import DataCleaner

# Creating an instance of the IndeedScraper class.
ISc = IndeedScraper(
    webdriver_path='./webdriver/chromedriver.exe',
    nb_pages=50,
    output_name="./data/INDEED.csv",
    min_delai=3,
    update_every=10
)

# Creating an instance of the WTTJScraper class.
wts = WTTJScraper(
    webdriver_path='./webdriver/chromedriver.exe',
    nb_pages=33,
    output_name="./data/WTTJ.csv",
    update_every=10,
)

# Creating a list of threads and then appending the threads to the list.
thread_list = []
thrd1 = Thread(target=ISc.launch_scraping)
thrd2 = Thread(target=wts.launch_scraping)
thread_list.append(thrd1)
thread_list.append(thrd2)

# Starting the threads.
for t in thread_list:
    t.start()

# Waiting for the threads to finish before continuing the execution of the code.
for t in thread_list:
    t.join()

# Delay to wait the creation of the csv.
time.sleep(3)

# Reading the csv files and concatenating them.
df1 = pd.read_csv("./data/INDEED.csv")
df2 = pd.read_csv("./data/WTTJ.csv")
df3 = pd.concat([df1, df2], axis=0, ignore_index=True)

# This is checking if the file exists, if it does, it will read the file and concatenate it with the new data. If it
# doesn't, it will just write the new data to the file.
# It makes one csv containing all the job offers that we have scraped.
if os.path.isfile('./data/Ind_Wttj.csv')==True :
    df4 = pd.read_csv('./data/Ind_Wttj.csv')
    df_final = pd.concat([df4,df3],axis=0,ignore_index=True)
    df_final.to_csv('./data/Ind_Wttj.csv',index=False)
else :
    df3.to_csv('./data/Ind_Wttj.csv', index=False)


# Creating an instance of the DataCleaner class and then calling the clean method on it.
dc = DataCleaner('./data/Ind_Wttj.csv')
dc.clean('./clean_data/clean_data.csv')
