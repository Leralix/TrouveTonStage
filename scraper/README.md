# Scraping process
Basically in the precedent README, the way to execute the scraping process is explained, this one will be more about explanation.
So, for now the project is made of 2 scrapers, one for Welcome To The Jungle and one for Indeed.

## The process
The process is made using multi-thread to run the 2 scrapers at once, and be more efficient.
### Gathering Informations
You guessed it but to gather the informations we used scrapers on different websites.
The main problem encountered was the websites them-selves, because they block basic scraper, so we had to use Selenium in both ones.

The process used in both is merely the same, it first gather information, and produce a 'csv' file stocked inside the 'data' folder.
For both scrapers there's one useful parameters called 'update_every' that creates a temporary version of the final csv in cause an error occure, we have anemergency file containing all the progress made.
#### Welcome To The Jungle
Because this website in strange enough with the way of changing pages, the process is unusual because there is no specific URL for each pages, so we can't have a recurrent URL to put in a for loop.
However, if we stay on the same page all along and change page we can take all the links of job offers. It can be sumed up as:
1. Get on the main page
2. Gather links of all job offers on this page
3. Click on the next button page and gather all the links from job offers
4. Do the same for the next page, and for the next...
5. Once all the links were all gathered we scrap each one of them to take the informations

Because the process is dependent on going on every page and then scrpaing the links, there can be an error. So we store the links taken from page in 'data/temp/temp_wttj_links.csv'.
And this 'csv' can be put inside the WTTJScraper in the parameters to not scrap every page on the website and take immediately links of the offers, it gains some time.

The gathering of information was pretty easy as Welcome To The Jungle present information clearly.

#### Indeed
The process used for Indeed in fairly simple:
1. Go on a page
2. Take every job offers link on the page
3. Go on every links and scrap informations
4. Go on the next page and do the same
5. And so on...

The only huge problem in this scraper was gathering the informations. Unlike WTTJ which contains a clear field for the degree, Indeed haven't.
So we used REGEX to get informations like this one, it's maybe not precise, but we developped good REGEX that match most of the situation in job offers, as the structure of job offer on Indeed are nearly the same.
### Cleaning
Once the 2 scrapers are done, they store the result in "data" folder, and 'regular' update in 'data/temp'.
We can append the 2 files together, and clean the datas all at once with the DataCleaner instance.

### Have an output
After the data cleaned, we export it into a 'csv' file.
This file can be used for the 'app' by moving the data cleaned from 'scraper/data/clean_data/name_given.csv' to 'app/data/name_given.csv'

