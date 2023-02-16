# It creates a connection to an elasticsearch server, and adds data from a csv file to it
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pandas as pd
import time

use_these_keys = ['Titre', 'Durée', 'Duree_format', 'Description', 'Nom entreprise', 'BacFormat', 'Deb_format',
                  'ContratFormat', 'url']


class ElasticConnection:
    def __init__(self,csv_filepath,local:bool=False,port:int=9200):
        """
        This function initializes the class by setting the filepath to the csv file, the port number of an elasticsearch docker images, and the local flag

        Args:
          csv_filepath: The path to the CSV file you want to import into Elasticsearch.
          local (bool): If you're running Elasticsearch locally, set this to True. Defaults to False
          port (int): The port number that Elasticsearch is running on. Defaults to 9200
        """
        self.LOCAL=local
        self.port = port
        self.csv_filepath = csv_filepath
        self.es_client=None
        self.df=None

    def create_connection(self):
        """
        It creates a connection to the Elasticsearch server, and then adds the data from the csv file to the server

        Returns:
          The elasticsearch client
        """
        print("Connexion to host")


        # It's creating a connection to the elasticsearch server. If the local flag is set to True, it will connect to the
        # localhost, otherwise it will connect to the elasticsearch docker image.
        if self.LOCAL==True:
            self.es_client = Elasticsearch(hosts=["http://localhost:"+str(self.port)])
        else:
            self.es_client = Elasticsearch(hosts=["http://elasticsearch:"+str(self.port)])


        # It's waiting for the elasticsearch server to be ready before trying to connect to it.
        time.sleep(0.1)
        print("Start Ping")
        time.sleep(0.2)
        self.es_client.ping()
        print("End Ping")

        # It's reading the csv file and filling the empty cells with an empty string.
        self.df = pd.read_csv(self.csv_filepath)
        self.df = self.df.fillna('')


        # It's printing the ping of the elasticsearch server, and then it's adding the data from the csv file to the
        # server.
        print(self.es_client.ping())
        self.add_data_()
        return self.es_client

    def filterKeys(self,document):
        """
        It takes a dictionary as an argument and returns a new dictionary with only the keys specified in the list
        use_these_keys

        Args:
          document: The document to be filtered.

        Returns:
          A dictionary with the keys that are in the list use_these_keys
        """
        return {key: document[key] for key in use_these_keys}


    def doc_generator(self,df):
        """
        It takes a dataframe and returns a generator that yields a dictionary for each row in the dataframe

        Args:
          df: the dataframe that contains the data you want to index
        """
        df_iter = df.iterrows()

        # It's iterating through the dataframe and creating a dictionary for each row in the dataframe.
        # In ElasticSearch the index will be 'job_offer' and each one will be identified thanks to the 50 last characters of its url.
        for index, document in df_iter:
            yield {
                "_index": 'job_offer',
                "_type": "offer",
                "_id": document['url'][:50],
                "_source": self.filterKeys(document),
            }

    def add_data_(self):
        """
        It takes a dataframe, converts it to a generator, and then uses the bulk function from the elasticsearch-helpers
        library to add the data to the index.
        """
        helpers.bulk(self.es_client, self.doc_generator(self.df))
