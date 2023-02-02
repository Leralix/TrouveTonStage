import re
from bs4 import BeautifulSoup

# Declaration of all the regex that will be use to extract:
# bac/diploma required, job duration, beginning month of the offer and salary if indicated.

regex_BAC_3 = re.compile(
    r"(\sCAP\s|\sIUT\s|\sLicence\s|\sMaster(\s*\d{1}|)\s|\sDUT\s|\sBTS\s|\sBEP\s|\sbaccalauréat\s|\s*M1\s*|\s*M2\s*|\s*Grande.?\sEcole|\s*stage.{1,10}fin.{1,10}étude|Formation(?:.{1,20})ieur)",
    re.I | re.UNICODE)
regex_BAC_1 = re.compile(r"(?:préparez.+?|De\s*)(bac.{1,5}(à|\/)\s*bac.+?(\d|pro))", re.I | re.UNICODE)
regex_BAC_2 = re.compile(
    r"(?:Formation|profil|prérequis|requis|études|titulaire)(?:[\s\S]{1,70})(Bac(pro|\s*[+\s*]\s*.{0,5}\d))",
    re.I | re.UNICODE)
regex_BAC = [regex_BAC_1, regex_BAC_2, regex_BAC_3]

regex_duree2 = re.compile(r"(?:Durée|durée|stage|Stage|période)(?:.{1,60})(\d{1}(\s*)mois)", re.I | re.UNICODE)
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


# Function removing all html tags from a soup object.
# Parameters soup : beautiful soup object
# Returns : a string containing the text data inside the soup object
def remove_tags(soup):
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()

    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)


# Function retrieving information from a string containing the content of an HTML page from indeed.
# Parameters content: html code of a job offer on Indeed.
# Returns: dictionnary of different values extracted from this webpage like duration, diploma reuqired, salary...
def scrap_page(content):
    # Transform the content in a soup object to extract values
    soup = BeautifulSoup(content, 'html.parser')

    # Get the job type indicated on the page
    r = soup.find("div", {"id": "jobDetailsSection"})
    type_contrat = set()
    for section in soup.find_all('div', {"class": "css-1hplm3f eu4oa1w0"}):
        if section.find('div').text == "Type de contrat":
            for element in section.find_all('div')[1:]:
                type_contrat.add(element.text.lower())

    # And if not indicated, take the job title and look into it to find if it contains a job type.
    titre = soup.find("h1", {"class": "icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title"}).text

    type_contrat_base = ['alternance', 'cdd', 'cdi', 'stage']
    for mot in titre.split(' '):
        if mot.lower() in type_contrat_base:
            type_contrat.add(mot.lower())

    # Remove from the job types a recurrent one, which is not important.
    try:
        type_contrat.remove('temps plein')
        type_contrat.remove('télétravail')
    except:
        pass

    type_contrat_string = ','.join(type_contrat)

    # To retrieve all the other informations, will have to use the job description
    description = soup.find("div", {"id": "jobDescriptionText"})

    # Keep an original version without html tags but with multiplie line and another one with the content on a unique
    # line.
    description_text_original = description.text
    description_text = remove_tags(description)

    # Retrieve the diploma informations
    # Because an offer could have multiple requirement, the information is stored in a list.
    bac = []
    try:
        # For all the regex to retrieve the associated information
        for regex in regex_BAC:
            # Get all results
            result = (re.findall(regex, description_text))
            # If not empty add those to the list
            if result != []:
                bac += ([item[0] for item in result])
    except:
        pass

    bac_set = set(bac)
    bac_string = ','.join(bac_set)

    # Retrieve the duration information
    # Because an offer just have a unique duration, the information is stored in a string.
    duree = ""

    # For all the regex to retrieve the associated information
    for regex in regex_duree_list:
        # Get all results
        result = re.findall(regex, description_text)
        # If not empty add those to the list
        if result:
            print(result)
            duree = result[0][0]
            break

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
        pass

    # Retrieve the salary informations if existing
    # Try to match the regex and if not, the informations are empty
    try:
        salaire = (re.search(regex_salaire_compiled, description_text).group(1))
        periodicite_salaire = (re.search(regex_salaire_compiled, description_text).group(2))
    except:
        salaire = ""
        periodicite_salaire = ""

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

    # Return all the informations gathered into a dictionnary.
    # The keys will be the column names of the future dataset.
    return {
        "Titre": [titre],
        "Type de contrat": [type_contrat_string],
        "Bac": [bac_string],
        "Durée": [duree],
        "Début": [debut],
        "Nom entreprise": [nom_company],
        "Localisation": [localisation],
        "Description": [description_text_original],
        "Salaire": [salaire],
        "Period. salaire": [periodicite_salaire]
    }
