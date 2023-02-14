from elasticsearch import Elasticsearch
from elasticsearch import helpers

import pandas as pd
import time

use_these_keys = ['Titre', 'Durée', 'Duree_format', 'Description', 'Nom entreprise', 'BacFormat', 'Deb_format',
                  'ContratFormat', 'url']


class ElasticConnection:
    def __init__(self,csv_filepath,local:bool=False,port:int=9200):
        self.LOCAL=local
        self.port = port
        self.csv_filepath = csv_filepath
        self.es_client=None
        self.df=None

    def create_connection(self):
        print("Connection a l'host")


        if self.LOCAL==True:
            self.es_client = Elasticsearch(hosts=["http://localhost:"+str(self.port)])
        else:
            self.es_client = Elasticsearch(hosts=["http://elasticsearch:"+str(self.port)])


        time.sleep(0.1)
        print("début du ping")
        time.sleep(0.2)
        self.es_client.ping()
        print("fin du ping")

        self.df = pd.read_csv(self.csv_filepath)
        self.df = self.df.fillna('')


        print(self.es_client.ping())
        self.add_data_()
        return self.es_client

    def filterKeys(self,document):
        return {key: document[key] for key in use_these_keys}


    def doc_generator(self,df):
        df_iter = df.iterrows()
        for index, document in df_iter:
            yield {
                "_index": 'job_offer',
                "_type": "offer",
                #Id aussi fonctin de hashage ??
                "_id": document['url'][:50],
                "_source": self.filterKeys(document),
            }

    def add_data_(self):
        helpers.bulk(self.es_client, self.doc_generator(self.df))
