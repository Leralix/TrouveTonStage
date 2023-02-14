from elasticsearch import Elasticsearch
from elasticsearch import helpers

import pandas as pd
import time

print("Connection a l'host")
LOCAL = True
if LOCAL==True:
    es_client = Elasticsearch(hosts=["http://localhost:9200"])
else:
    es_client = Elasticsearch(hosts=["http://elasticsearch:9200"])
time.sleep(0.1)
print("début du ping")
time.sleep(0.2)
es_client.ping()
print("fin du ping")

df = pd.read_csv("data/clean_data.csv")
df = df.fillna('')

use_these_keys = ['Titre', 'Durée','Duree_format','Description', 'Nom entreprise', 'BacFormat','Deb_format','ContratFormat','url']

print(es_client.ping())

def filterKeys(document):
    return {key: document[key] for key in use_these_keys}


def doc_generator(df):
    df_iter = df.iterrows()
    for index, document in df_iter:
        yield {
            "_index": 'job_offer',
            "_type": "offer",
            #Id aussi fonctin de hashage ??
            "_id": document['url'][:50],
            "_source": filterKeys(document),
        }

print("Ajout fini")
print(helpers.bulk(es_client, doc_generator(df)))
