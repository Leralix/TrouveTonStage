import pandas as pd
import numpy as np
import re

bac_replace = {
    "bac":"bac",
    "bts":"bts",
    "stagedefind’étude":"bac+5",
    "baccalauréat":"bac",
    "bac+4/5":"bac+4",
    "master":"bac+5",
    "formationsupérieur":"bac+5",
    "licence":"bac+3",
    "bac+4/+5":"bac+4",
    "bac+4/5":"bac+4",
    "bac+2/3":"bac+2",
    "bac+3/4":'bac+3',
    "cap":'cap',
    "bep":"bep",
    "dut":'dut',
    "sansdiplôme":"sans diplome",
    "bac+2":"bac+2",
    "bac+1":"bac+1",

    "bac+3":'bac+3',
    "bac+4":"bac+4",
    "bac+5":"bac+5",
    "master1":"bac+4",
    "master2":"bac+5",
    "que possible": "dès que possible"

}


month_dict = {

    "01": "Janvier",
    "02": "Février",
    "03": "Mars",
    '04': 'Avril',
    '05': 'Mai',
    '06': 'Juin',
    '07': "Juillet",
    '08': "Aout",
    "09": "Septembre",
    "10": "Octobre",
    "11": "Novembre",
    "12": "Décembre"
}

regex_date1=r'\d{2}\/\d{2}\/202[0-9]'
regex_date2=r"\w+\s\d{4}"


class DataCleaner:

    def __init__(self,filename,output_name):
        try:
            self.df = pd.read_csv(filename)
            self.data_cleaning()
            self.to_csv(output_name)
        except:
            raise "File is not a csv"


    def clean_bac_(self, a):
        a = a.replace(' / ', ',').split(',')

        a_set = set([item.strip().lower().replace(' ', '') for item in a])
        items = []
        for item in a_set:
            if item in bac_replace.keys():
                item = bac_replace[item]
                items.append(item)

        if items == []:
            return ""
        if 'cap' in items:
            return 'cap'
        if 'bep' in items:
            return 'bep'
        if 'bts' in items:
            return 'bts'
        if 'dut' in items:
            return 'dut'
        if 'bac' in items:
            return 'bac'
        if 'bac+2' in items:
            return 'bac+2'
        if 'bac+3' in items:
            return 'bac+3'
        if "bac+4" in items:
            return 'bac+4'
        if 'bac+5' in items:
            return 'bac+5'





        else:
            return items[0]


    def clean_debut_(self, a):
        if re.match(regex_date1, a) != None:
            a_split = a.split('/')
            month = month_dict[a_split[1]]
            year = a_split[-1]
            return str(month).lower() + ' ' + str(year).lower()
        elif re.findall(regex_date2, a) != []:
            return re.findall(r"\w+\s\d{4}", a)[0].lower()
        else:
            return a

    def data_cleaning(self):

        self.df.replace('Non spécifié', np.nan)
        self.df.drop_duplicates(inplace=True)

        self.df['BacFormat'] = self.df["Bac"].fillna('').apply(lambda x: self.clean_bac_(x))
        self.df['Deb_format'] = self.df["Début"].fillna('').apply(lambda x: self.clean_debut_(x))
        self.df['ContratFormat'] = self.df['Type de contrat'].apply(lambda x: x.lower())

    def to_csv(self,filename:str):
        return self.df.to_csv(filename)






