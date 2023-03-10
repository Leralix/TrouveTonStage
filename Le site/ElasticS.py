from elasticsearch import Elasticsearch
from elasticsearch import helpers

import pandas as pd

LOCAL = False


es_client = Elasticsearch(hosts=["http://localhost:9200"])
es_client.ping()

df = pd.read_csv("DatabaseFInaleWTTJ.csv")
df = df.fillna('')

use_these_keys = ['Titre', 'Durée', 'Nom entreprise', 'Bac','url']


def filterKeys(document):
    return {key: document[key] for key in use_these_keys}


def doc_generator(df):
    df_iter = df.iterrows()
    for index, document in df_iter:
        doc = filterKeys(document)
        yield {
            "_index": 'job_offer',
            "_type": "offer",
            "_id": doc['url'],
            "_source": doc,
        }


print(es_client.ping())
print(helpers.bulk(es_client, doc_generator(df)))
print("FINI !!")
