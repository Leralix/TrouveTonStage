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
        self.content = page_source

    # Function removing all html tags from a soup object.
    # Parameters soup : beautiful soup object
    # Returns : a string containing the text data inside the soup object
    @staticmethod
    def remove_tags_(soup):
        for data in soup(['style', 'script']):
            # Remove tags
            data.decompose()

        # return data by retrieving the tag content
        return ' '.join(soup.stripped_strings)

    # Function retrieving information from a string containing the content of an HTML page from indeed.
    # Parameters content: html code of a job offer on Indeed.
    # Returns: dictionnary of different values extracted from this webpage like duration, diploma reuqired, salary...
    def scrap_page(self):
        # Transform the content in a soup object to extract values
        soup = BeautifulSoup(self.content, 'html.parser')

        job_title = soup.find("h1", {"class": "icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title"}).text

        # To retrieve all the other informations, will have to use the job description
        description = soup.find("div", {"id": "jobDescriptionText"})

        # Keep an original version without html tags but with multiplie line and another one with the content on a
        # unique line.
        description_text_original = description.text
        description_text = self.remove_tags_(description)

        job_type = self.job_type_(soup, job_title)

        job_bac = self.job_bac_(description_text)
        job_duration = self.job_duration_(description_text)
        job_debut = self.job_debut_(description_text)
        company_name, company_localisation = self.job_company_info_(soup)

        job_description = description_text_original

        job_salary, salary_periodicity = self.job_salaire_(description_text)

        # Return all the informations gathered into a dictionnary.
        # The keys will be the column names of the future dataset.
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

    # Type contrat
    @staticmethod
    def job_type_(soup, titre):
        # Get the job type indicated on the page
        type_contrat = set()
        for section in soup.find_all('div', {"class": re.compile('.*css-.*')}):
            # for section in soup.find_all('div', {"class": "css-1hplm3f eu4oa1w0"}):
            try:
                if section.find('div').text == "Type de contrat":
                    for element in section.find_all('div')[1:]:
                        type_contrat.add(element.text.lower())
            except:
                continue
        type_contrat_base = ['alternance', 'cdd', 'cdi', 'stage']
        for mot in titre.split(' '):
            if mot.lower() in type_contrat_base:
                type_contrat.add(mot.lower())

        # Remove from the job types a recurrent one, which is not important.
        try:
            type_contrat.remove('temps plein')
            type_contrat.remove('télétravail')
        except Exception:
            pass
            # raise 'Cannot remove statement from job types'

        type_contrat_string = ','.join(type_contrat)

        return type_contrat_string

    # Salaire

    # Bac
    @staticmethod
    def job_bac_(description_text):
        # Retrieve the diploma informations
        # Because an offer could have multiple requirement, the information is stored in a list.
        bac = []
        try:
            # For all the regex to retrieve the associated information
            for regex in regex_BAC:
                # Get all results
                result = (re.findall(regex, description_text))
                # If not empty add those to the list
                if result:
                    bac += ([item[0] for item in result])
        except:
            raise 'No bac informations inside the offer'

        bac_set = set(bac)
        bac_string = ','.join(bac_set)

        return bac_string

    # Durée
    @staticmethod
    def job_duration_(description_text):
        # Retrieve the duration information
        # Because an offer just have a unique duration, the information is stored in a string.
        duree = ""

        # For all the regex to retrieve the associated information
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
        # Retrieve the beginning date information
        # Because an offer has a unique beginning date, the information is stored in a string.
        debut = ""
        try:
            # For all the regex to retrieve the associated information
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
        # Retrieve the salary informations if existing
        # Try to match the regex and if not, the informations are empty
        try:
            salaire = (re.search(regex_salaire_compiled, description_text).group(1))
            periodicite_salaire = (re.search(regex_salaire_compiled, description_text).group(2))
        except:
            salaire = ""
            periodicite_salaire = ""

        return salaire, periodicite_salaire

    @staticmethod
    def job_company_info_(soup):

        # Retrieve the company informations such as: name and location.
        # Because the name could be located in 2 different ways, try the first otherwise the second
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
        if len(localisation_info) == 12:
            localisation = localisation_info[-2].text
        else:
            localisation = localisation_info[-3].text

        return nom_company, localisation
