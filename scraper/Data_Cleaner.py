import pandas as pd
import numpy as np
import re

from unidecode import unidecode

bac_replace = {
    "bac": "bac",
    "bts": "bts",
    "iut": "iut",
    "stagedefind’étude": "bac+5",
    "baccalauréat": "bac",
    "bac+4/5": "bac+4",
    "master": "bac+5",
    "formationsupérieur": "bac+5",
    "licence": "bac+3",
    "bac+4/+5": "bac+4",
    "bac+2/3": "bac+2",
    "bac+3/4": 'bac+3',
    "cap": 'cap',
    "bep": "bep",
    "dut": 'dut',
    "sansdiplôme": "sans diplome",
    "bac+2": "bac+2",
    "bac+1": "bac+1",

    "bac+3": 'bac+3',
    "bac+4": "bac+4",
    "bac+5": "bac+5",
    "master1": "bac+4",
    "master2": "bac+5",
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

regex_date1 = r'\d{1,2}\/\d{2}\/202[0-9]'
regex_date2 = r"\w+\s\d{4}"


class DataCleaner:

    def __init__(self, filename):
        try:
            self.df = pd.read_csv(filename)
        except:
            raise "File is not a csv"

    def clean(self, output_name):
        self.data_cleaning()
        self.to_csv(output_name)

    @staticmethod
    def clean_bac_(a):
        a = a.replace(' / ', ',').split(',')

        a_set = set([item.strip().lower().replace(' ', '') for item in a])
        items = []
        for item in a_set:
            if item in bac_replace.keys():
                item = bac_replace[item]
                items.append(item)

        if not items:
            return ""
        if 'cap' in items:
            return 'cap'
        if 'bep' in items:
            return 'bep'
        if 'bts' in items:
            return 'bts'
        if 'dut' in items:
            return 'dut'
        if 'iut' in items:
            return 'iut'
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

    @staticmethod
    def clean_debut_(a):
        a = str(a)
        a = unidecode(a)
        a = a.strip()

        if 'possible' in a:
            return "Dès que possible"
        if ('semestre' in a) | ('trimestre' in a):
            return a.lower()
        elif ('à' in a) | ('au' in a):
            return np.nan
        elif re.search(r"(?:de|pour|debut)(?:\s*)(\d{4})", a):
            return re.search(r"(?:de|pour|debut)(?:\s*)(\d{4})", a).group(1)
        elif re.findall(r'\d{1,2}\/\d{2}\/202[0-9]', a):
            tmp = re.findall(r'\d{1,2}\/\d{2}\/202[0-9]', a)[0]
            a_split = tmp.split('/')
            month = unidecode(month_dict[a_split[1]])
            year = a_split[-1]
            return str(month).lower() + ' ' + str(year).lower()
        elif re.findall(r"\w+\s\d{4}", a):
            if re.search(r"(\w+)(?:\s\d{4})", a).group(1).strip().lower() in ['janvier', 'février', "fevrier", 'mars',
                                                                              "avril", "mai", "juin", "juillet", "aout",
                                                                              "août", "septembre", "octobre",
                                                                              "novembre", "décembre", "decembre"]:
                return re.findall(r"\w+\s\d{4}", a)[0].lower()
        else:
            return np.nan

    def clean_duree_(self,a):
        a = str(a)
        a = unidecode(a)

        search1 = re.search(r"(\d{1,2})\s*a\s*(\d{1,2})\s*(?:mois)", a)
        search2 = re.search(r"(\d{1,2})\s*(?:mois)", a)

        if search1 is not None:
            if int(search1.group(1)) < int(search1.group(2)):
                return str(list(range(int(search1.group(1)), int(search1.group(2)) + 1)))
            else:
                return str(list(range(int(search1.group(2)), int(search1.group(1)) + 1)))
        if search2:
            return int(search2.group(1))

    def data_cleaning(self):

        self.df.replace('Non spécifié', np.nan)
        self.df.drop_duplicates(inplace=True)

        self.df['BacFormat'] = self.df["Bac"].fillna('').apply(lambda x: self.clean_bac_(x))
        self.df['Deb_format'] = self.df["Début"].fillna('').apply(lambda x: self.clean_debut_(x))
        self.df['ContratFormat'] = self.df['Type de contrat'].fillna('').apply(lambda x: x.lower())
        self.df['Duree_format'] = self.df['Durée'].fillna('').apply(lambda x: self.clean_duree_(x))

    def to_csv(self, filename: str):
        return self.df.to_csv(filename,index=False)
