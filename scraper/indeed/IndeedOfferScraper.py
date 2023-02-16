import re
from bs4 import BeautifulSoup

# Declaration of all the regex that will be use to extract:
# bac/diploma required, job duration, beginning month of the offer and salary if indicated.
regex_BAC_3 = re.compile(
    r"(\sCAP\s|\sIUT\s|\sLicence\s|\sMaster(\s*\d{"
    r"1}|)\s|\sDUT\s|\sBTS\s|\sBEP\s|\sbaccalauréat\s|\s*M1\s*|\s*M2\s*|\s*Grande.?\sEcole|\s*stage.{1,10}fin.{1,"
    r"10}étude|Formation(?:.{1,20})ieur)",
    re.I | re.UNICODE)
regex_BAC_1 = re.compile(r"(?:préparez.+?|De\s*)(bac.{1,5}(à|\/)\s*bac.+?(\d|pro))", re.I | re.UNICODE)
regex_BAC_2 = re.compile(
    r"(?:Formation|profil|prérequis|requis|études|titulaire|prépa)(?:[\s\S]{1,150})(Bac(\s*|pro|\s*[+\s*]\s*.{0,5}\d))",
    re.I | re.UNICODE)
regex_BAC = [regex_BAC_1, regex_BAC_2, regex_BAC_3]

regex_duree2 = re.compile(r"(?:Durée|durée|stage|Stage|période)(?:.{1,60})(\s\d+(\s*)mois)", re.I | re.UNICODE)
regex_duree1 = re.compile(r"(?:Durée|durée|stage|Stage|période)(?:.{1,60})(\d{1}\s(mois|)\s*à\s\d{1}\smois)",
                          re.I | re.UNICODE)
regex_duree_list = [regex_duree1, regex_duree2]

regex_debut2 = re.compile(r"(?:Début|début)(?:\s*(?:[:]|)\s*)(?:\S{0,20})(\s*(\S{1,60})\s*(à|et|\/|-).{1,60}\s*202["
                          r"0-9])", re.I | re.UNICODE)
regex_debut3 = re.compile(r"(?:Début|dès|démarrage|début|à partir|prise\s*de\s*fonction|à po(?:.+?)ir)(?:.{1,"
                          r"60})(\b\w+\b\s202[3-9]|\d{2}\/\d{2}\/202[0-9])", re.I | re.UNICODE)
regex_debut1 = re.compile(
    r"(?:Début|dès|début|à partir|prise\s*de\s*fonction|à po(?:.+?)ir)(?:.{0,60})(d[éèe]s\sque\spossible)",
    re.I | re.UNICODE)
regex_DEBUT = [regex_debut1, regex_debut2, regex_debut3]

regex_salaire = r"(?:Salaire|Gratification)(?:.{1,30})[:](.{1,30})(?:\s*(?:par|\/)\s*)(mois|an)"
regex_salaire_compiled = re.compile(regex_salaire, re.I | re.UNICODE)


class IndeedOfferScraper:

    def __init__(self, page_source: str):
        """
        The function __init__() is a constructor that initializes the class of IndeedOfferScraper.

        Args:
          page_source (str): The HTML source of the page you want to parse (offer from Indeed).
        """
        self.content = page_source


    @staticmethod
    def remove_tags_(soup):
        """
        It removes all the tags from the html document and returns the text content

        Args:
          soup: the BeautifulSoup object

        Returns:
          the text of the html file.
        """

        # It removes all the tags from the html document and returns the text content
        for data in soup(['style', 'script']):
            data.decompose()

        return ' '.join(soup.stripped_strings)


    def scrap_page(self):
        """
        It takes the content of a page, transforms it into a soup object, extracts the information we want, and returns a
        dictionary with the information (job offer title, offer type, degree...)

        Returns:
          A dictionary with the keys being the column names of the future dataset.
        """

        # Parsing the HTML content of the page.
        soup = BeautifulSoup(self.content, 'html.parser')

        # Finding the title of the job and the description of the job.
        job_title = soup.find("h1", {"class": "icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title"}).text
        description = soup.find("div", {"id": "jobDescriptionText"})


        # Removing the tags from the html document and returning the text content.
        description_text_original = description.text
        description_text = self.remove_tags_(description)

        # Calling the functions associated to the information wanted.
        job_type = self.job_type_(soup, job_title)
        job_bac = self.job_bac_(description_text)
        job_duration = self.job_duration_(description_text)
        job_debut = self.job_debut_(description_text)
        company_name, company_localisation = self.job_company_info_(soup)
        job_description = description_text_original
        job_salary, salary_periodicity = self.job_salaire_(description_text)


        # Returning a dictionary with the keys being the column names of the future dataset.
        return {
            "Titre": [job_title],
            "Type de contrat": [job_type],
            "Bac": [job_bac],
            "Durée": [job_duration],
            "Début": [job_debut],
            "Nom entreprise": [company_name],
            "Localisation": [company_localisation],
            "Description": [job_description],
            "Salaire": [job_salary],
            "Period. salaire": [salary_periodicity]
        }

    @staticmethod
    def job_type_(soup, titre):
        """
        It takes the soup and the title of the job offer, and returns the type of contract

        Args:
          soup: the soup object of the page
          titre: the title of the job

        Returns:
          A string of the job types.
        """

        type_contrat = set()
        # Looking for the type of contract in the job offer.
        for section in soup.find_all('div', {"class": re.compile('.*css-.*')}):
            try:
                # Looking for the type of contract in the job offer section called 'Type de contrat'.
                if section.find('div').text == "Type de contrat":
                    for element in section.find_all('div')[1:]:
                        type_contrat.add(element.text.lower())
            except:
                continue

        # Looking for the type of contract in the job offer title.
        type_contrat_base = ['alternance', 'cdd', 'cdi', 'stage']
        for mot in titre.split(' '):
            if mot.lower() in type_contrat_base:
                type_contrat.add(mot.lower())


        # Removing the words 'temps plein' and 'télétravail' from the list of job types.
        # These words appends to appears in the 'Type de contrat' section, so we remove it.
        try:
            type_contrat.remove('temps plein')
            type_contrat.remove('télétravail')
        except Exception:
            pass

        # Joining the elements of the set type_contrat with a comma.
        type_contrat_string = ','.join(type_contrat)

        return type_contrat_string


    @staticmethod
    def job_bac_(description_text):
        """
        It takes a string as input (job description), and returns the degree required inside the job description

        Args:
          description_text: the text of the job description

        Returns:
          A string of the degree requirements
        """
        bac = []

        # Trying to find all the regex in the description text matching with the degree and if it finds it, it adds it to the list.
        try:
            # For all the regex to retrieve the associated information (degree)
            for regex in regex_BAC:
                # Get all results
                result = (re.findall(regex, description_text))
                # If not empty add those to the list
                if result:
                    bac += ([item[0] for item in result])
        except:
            raise 'No bac informations inside the offer'

        # Removing duplicates from the list of bac requirements.
        bac_set = set(bac)
        bac_string = ','.join(bac_set)

        return bac_string

    @staticmethod
    def job_duration_(description_text):
        """
        It takes a string as input (job description), and returns the degree required inside the job duration (in months)

        Args:
          description_text: the text of the job description

        Returns:
          A string containing the duration of the job offer.
        """
        duree = ""

        # For all the regex to retrieve the associated information (job duration)
        for regex in regex_duree_list:
            # Get all results
            result = re.findall(regex, description_text)
            # If not empty add those to the list
            if result:
                duree = result[0][0].strip()
                break

        return duree

    @staticmethod
    def job_debut_(description_text):
        """
        It takes a string as input (job description), and returns the job beginning date inside the job description

        Args:
          description_text: the text of the job offer

        Returns:
          A string containing the beginning date of the job offer.
        """
        debut = ""

        # Trying to find the beginning date of the job offer.
        try:
            # For all the regex to retrieve the associated information (beginning date)
            for regex in regex_DEBUT:
                # Get all results
                result = (re.search(regex, description_text))
                # If not empty add those to the list
                if result is not None:
                    debut = result.group(1)
                    break
        except:
            raise 'Job beginning date not inside offer'

        return debut

    @staticmethod
    def job_salaire_(description_text):
        """
        It takes a string as input (job description), and returns the salary inside the job description

        Args:
          description_text: the text of the job description

        Returns:
          the salary and the periodicity of the salary.
        """

        # Trying to find the salary and the periodicity of the salary. If it does not find it, it returns an empty string.
        # Use regex to find these informations.
        try:
            salaire = (re.search(regex_salaire_compiled, description_text).group(1))
            periodicite_salaire = (re.search(regex_salaire_compiled, description_text).group(2))
        except:
            salaire = ""
            periodicite_salaire = ""

        return salaire, periodicite_salaire

    @staticmethod
    def job_company_info_(soup):
        """
        It takes a soup object as input and returns the name and location of the company

        Args:
          soup: the soup object of the page

        Returns:
          the name of the company and the location of the job.
        """

        # Trying to find the name of the company. If it does not find it, it returns the name of the company.
        try:
            nom_company = soup.find('div', {
                'class': "jobsearch-InlineCompanyRating icl-u-xs-mt--xs jobsearch-DesktopStickyContainer-companyrating "
                         "css-11s8wkw eu4oa1w0"}).find(
                'a').text
        except:
            nom_company = soup.find('div', {
                'class': "jobsearch-InlineCompanyRating icl-u-xs-mt--xs jobsearch-DesktopStickyContainer-companyrating "
                         "css-11s8wkw eu4oa1w0"}).find_all(
                'div')[-4].text

        # Get the location according to the page structuration.
        localisation_info = soup.find('div', {
            "class": "icl-u-xs-mt--xs icl-u-textColor--secondary jobsearch-JobInfoHeader-subtitle "
                     "jobsearch-DesktopStickyContainer-subtitle"}).find_all(
            'div')
        # These prevent gathering false informations, because the structure of job offers is different from one to another.
        if len(localisation_info) == 12:
            localisation = localisation_info[-2].text
        else:
            localisation = localisation_info[-3].text

        return nom_company, localisation
