import pandas as pd
import numpy as np
import re
from unidecode import unidecode

# A dictionary that contains the different degrees that can be found in the dataframe.
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

# A dictionary that contains the months in French.
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

# A regular expression that is used to find a date in the format "dd/mm/yyyy" or a word followed by a space
# and a 4-digit number (month followed by a year).
regex_date1 = r'\d{1,2}\/\d{2}\/202[0-9]'
regex_date2 = r"\w+\s\d{4}"


# It takes a csv file as input, cleans it, and outputs a csv file
class DataCleaner:
    def __init__(self, filename):
        """
        The function takes a filename as an argument and tries to read the file as a csv. If it fails, it raises an error

        Args:
          filename: The name of the file you want to read in.
        """
        try:
            self.df = pd.read_csv(filename)
        except:
            raise "File is not a csv"

    def clean(self, output_name):
        """
        This function takes in a dataframe and outputs a cleaned dataframe

        Args:
          output_name: the name of the output file
        """
        self.data_cleaning()
        self.to_csv(output_name)

    @staticmethod
    def clean_bac_(a):
        """
        This function clean the degree information
        It takes a string as input, and returns a string as output.
        It maps the degree information whatever its shape is, and returns a simple degree that will be easier to understand

        Args:
          a: the string to be cleaned

        Returns:
          A string
        """

        # Replacing the '/' with a comma and then splitting the string into a list.
        a = a.replace(' / ', ',').split(',')
        a_set = set([item.strip().lower().replace(' ', '') for item in a])

        items = []
        # Mapping the degree information whatever its shape is, and returns a simple degree that will be easier to
        # understand
        for item in a_set:
            if item in bac_replace.keys():
                item = bac_replace[item]
                items.append(item)

        # Classify the degree information to take the least important
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
        """
        This function clean the beginning date information

        - If the string contains the word "possible", return "Dès que possible"
        - If the string contains the word "semestre" or "trimestre", return the string in lowercase
        - If the string contains the word "à" or "au", return NaN
        - If the string contains the word "de" or "pour" or "debut" followed by a space and a 4-digit number, return the
        4-digit number
        - If the string contains a date in the format "dd/mm/yyyy", return the month and year in lowercase
        - If the string contains a word followed by a space and a 4-digit number, return the word and the 4-digit number in
        lowercase
        - Otherwise, return NaN


        Args:
          a: the string to be cleaned

        Returns:
          A string
        """


        # Converting the input to a string, removing accents and stripping the string.
        a = str(a)
        a = unidecode(a)
        a = a.strip()

        if 'possible' in a:
            return "Dès que possible"
        if ('semestre' in a) | ('trimestre' in a):
            return a.lower()
        elif ('à' in a) | ('au' in a):
            return np.nan
        # Looking for a string that contains the word "de" or "pour" or "debut" followed by a space and a 4-digit number,
        # and returns the 4-digit number
        elif re.search(r"(?:de|pour|debut)(?:\s*)(\d{4})", a):
            return re.search(r"(?:de|pour|debut)(?:\s*)(\d{4})", a).group(1)
        # Looking for a date in the format "dd/mm/yyyy" and returns the month and year in lowercase
        elif re.findall(r'\d{1,2}\/\d{2}\/202[0-9]', a):
            tmp = re.findall(r'\d{1,2}\/\d{2}\/202[0-9]', a)[0]
            a_split = tmp.split('/')
            month = unidecode(month_dict[a_split[1]])
            year = a_split[-1]
            return str(month).lower() + ' ' + str(year).lower()
        # Looking for a word followed by a space and a 4-digit number, and returns the word and the 4-digit number in
        # lowercase
        elif re.findall(r"\w+\s\d{4}", a):
            # Checking if the word before the 4 digit number is a month.
            if re.search(r"(\w+)(?:\s\d{4})", a).group(1).strip().lower() in ['janvier', 'février', "fevrier", 'mars',
                                                                              "avril", "mai", "juin", "juillet", "aout",
                                                                              "août", "septembre", "octobre",
                                                                              "novembre", "décembre", "decembre"]:
                return re.findall(r"\w+\s\d{4}", a)[0].lower()
        else:
            return np.nan

    def clean_duree_(self,a):
        """
        This function clean the duration information

        It takes a string as input, and returns a list of integers if the string contains a range of months, or a single
        integer if the string contains a single month

        Args:
          a: the string to be cleaned

        Returns:
          A list of integers
        """

        # Converting the input to a string, removing accents and stripping the string.
        a = str(a)
        a = unidecode(a)

        search1 = re.search(r"(\d{1,2})\s*a\s*(\d{1,2})\s*(?:mois)", a)
        search2 = re.search(r"(\d{1,2})\s*(?:mois)", a)

        # Checking if the string contains a range of months, and returns a list of integers if it does.
        if search1 is not None:
            if int(search1.group(1)) < int(search1.group(2)):
                return str(list(range(int(search1.group(1)), int(search1.group(2)) + 1)))
            else:
                return str(list(range(int(search1.group(2)), int(search1.group(1)) + 1)))
        # Checking if the string contains a number of months, and return the informations contained thanks to a regex.
        if search2:
            return int(search2.group(1))

    def data_cleaning(self):
        """
        It cleans the dataframe by replacing the 'Non spécifié' values with NaN, dropping duplicates, and cleaning the Bac,
        Début, Type de contrat, and Durée columns
        """

        self.df.replace('Non spécifié', np.nan)
        self.df.drop_duplicates(inplace=True)

        self.df['BacFormat'] = self.df["Bac"].fillna('').apply(lambda x: self.clean_bac_(x))
        self.df['Deb_format'] = self.df["Début"].fillna('').apply(lambda x: self.clean_debut_(x))
        self.df['ContratFormat'] = self.df['Type de contrat'].fillna('').apply(lambda x: x.lower())
        self.df['Duree_format'] = self.df['Durée'].fillna('').apply(lambda x: self.clean_duree_(x))

    def to_csv(self, filename: str):
        """
        This function takes a dataframe and a filename as input and saves the dataframe as a csv file with the given
        filename.

        Args:
          filename (str): The name of the file to be written to.

        Returns:
          The dataframe is being returned.
        """
        return self.df.to_csv(filename,index=False)
