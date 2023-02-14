import pandas as pd
import os
from Data_Cleaner import DataCleaner


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
