from elasticsearch.helpers import scan
from flask import Flask, render_template,request
from elasticsearch import Elasticsearch
import pandas as pd

app = Flask(__name__)


LOCAL = True

if LOCAL==True:
    es_client = Elasticsearch(hosts=["http://localhost:9200"])
else:
    es_client = Elasticsearch(hosts=["http://elasticsearch:9200"])

print("DEBUT")


@app.route('/')
def home():
    return render_template('main.html')



@app.route('/search_results', methods=['GET','POST'])
def search_request():

    search_term = request.form["NameInput"]
    contrat_term = request.form["ContratInput"]
    bac_req = request.form['bac_select']
    duration_req = request.form['duration_select']

    counter_term=0

    if search_term !="":
        counter_term +=1
    if contrat_term !="":
        counter_term +=1
    if bac_req!='0':
        counter_term +=1
    if duration_req !='0':
        counter_term +=1




    query = {
        "query": {
            "bool": {
                "should": [
                    {"multi_match": {
                        "query" : search_term,
                        "fields":["Description","Titre"] }},
                    {"match": {"ContratFormat": contrat_term}},
                    {"match": {"Duree_format": duration_req.replace(',', ' ')}},
                    {"term":{"BacFormat.keyword": bac_req}}

                ],
                "minimum_should_match": counter_term
            }
        }
    }
    rel = scan(client=es_client,
               query=query,
               scroll='1m',
               index='job_offer',
               raise_on_error=True,
               preserve_order=False,
               clear_scroll=True
               )
    result = list(rel)
    temp = []

    for hit in result:
        temp.append(hit['_source'])
    # Create a dataframe.
    data = pd.DataFrame(temp)
    #print(data)
    #data.to_csv("fichierCsvAthibaud")
    #print(result[8]['_source']['Titre'])
    return render_template('search_results.html', res=result)

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='0.0.0.0')
    #app.run(host='0.0.0.0', port=5000,debug = True)


