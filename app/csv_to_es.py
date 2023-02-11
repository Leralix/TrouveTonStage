from elasticsearch import Elasticsearch
from elasticsearch import helpers

import pandas as pd
import time

LOCAL = False


#es_client = Elasticsearch(hosts=["http://localhost:9200"])
print("Connection a l'host")
#es_client = Elasticsearch(hosts=["http://elasticsearch:9200"])
es_client = Elasticsearch(hosts=["http://localhost:9200"])
time.sleep(0.1)
print("début du ping")
time.sleep(0.2)
es_client.ping()
print("fin du ping")

df = pd.read_csv("data/clean_data.csv")
df = df.fillna('')

use_these_keys = ['Titre', 'Durée', 'Nom entreprise', 'BacFormat','url']

print(es_client.ping())

def filterKeys(document):
    return {key: document[key] for key in use_these_keys}


def doc_generator(df):
    df_iter = df.iterrows()
    for index, document in df_iter:
        yield {
            "_index": 'job_offer',
            "_type": "offer",
            "_id": document['url'][:50],
            "_source": filterKeys(document),
        }

print("Ajout fini")
print(helpers.bulk(es_client, doc_generator(df)))
