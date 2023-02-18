# Project : TrouveTonStage

![GitHub contributors](https://img.shields.io/github/contributors/Leralix/TrouveTonStage?label=Contributeur)

---
# Sommaire :
1. [Description ](#desc)
2. [Installation ](#install)
3. [Usage ](#usage)
4. [Documentation ](#docu)
5. [Notes ](#notes)
---

<a name="desc"></a>
## Description
Project carried out as a part of a Data Engineering unit at ESIEE Paris.
The goal behind was to collect data and reuse it through databases, and produce value with graphic interpretation or search engine.

This project called "TrouveTonStage" aims to make the search for an internship simpler and more personalized. 
It's made of few scrapers which first gather information about job offers on differents websites. 
Once done, these data stored in csv are then put on an ElasticSearch database, and thanks to some Flask, a searchengine is build upon that to provide an efficient way to navigate through all theses job offers according to criterions.

For the technical part, you can look to the readme file in the 'scraper' file which contains all scraper used.

<a name="install"></a>
## Installation
If you want to use these project, you can first clone the repo:
<code>
git clone https://github.com/Leralix/TrouveTonStage.git
</code>

### Scrapig part
The scraping part in inside de 'scraper' folder.
There is one requirement about the scraping part if you want to run this, you have to install additional packages contained in "requirements.txt"
<code>
$ python -m pip install -r requirements.txt
</code>

### Application part
The application part is inside the 'app' folder.
To install correctly the application part, you have to get Docker, because here we use an image of ElasticSearch.
You have two choices to run the backend process, either you have a simple image of ElasticSearch and you run the programm locally or you run the docker-compose. 



## Usage
### Getting informations
To execute correctly the project, you can first execute the 'main.py' inside the "scraper" folder that will execute the scripts to gather informations about job offers.
Inside the main you can modify the delay between each pages load, the number of pages to scrap, output files and other things.
Once the data is gathered, it cleans all these datas and produce an output csv.
You can run it with :
<code>
$ python main.py
</code>

Edit: Be careful, the process can take quite a time to run entierly, so make sur you have time or you scrap few pages.

The scraping process is made so that every time the 'main' file is executed, it stores the informations in only one csv that kept incrementing with new datas.

### Run the backend
The folder 'app' contains everything to run the backend process. The 'data' folder contains the csv that will be put on ES, so make sure you transfer the csv collected from the scraper to the 'app' folder.

Make sure you launch docker, then go inside the 'app' folder and type:
<code>
docker-compose up -d
</code>

This will execute the docker-compose file. 
Wait few seconds, its the time it takes to put all datas in csv to ES, then go on your :5000 port to see the Flask page.





<a name="docu"></a>
## Documentation
The documenation was produced with Sphinx and is contained inside the 'docs' folder.
### [See Documentation](https://htmlpreview.github.io/?https://github.com/Leralix/TrouveTonStage/blob/Test-Gab-Thibaud/docs/build/html/index.html)

If the link doesn't work well, you can easily go to
<code>
docs/build/html
</code>
And open the "index.html" inside, and normally you'll have no problem to see the documentation.


<a name="notes"></a>
## Note

- The docstring was made using help of the "Mintlify Doc Writer" plugin in PyCharm.
- The dockerisation of the 'app' can be changed by using a volume instead of keeping everything local