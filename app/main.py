from csv_to_es import ElasticConnection
from elasticsearch.helpers import scan
from flask import Flask, render_template,request
from elasticsearch import Elasticsearch
import pandas as pd


esc = ElasticConnection(csv_filepath='data/clean_data.csv',local=False).create_connection()



app = Flask(__name__)
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
        rel = scan(client=esc,
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

        return render_template('search_results.html', res=result)

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='0.0.0.0')
