from elasticsearch.helpers import scan
from flask import Flask, render_template,request
from elasticsearch import Elasticsearch
import pandas as pd

app = Flask(__name__)

es_client = Elasticsearch(hosts=["http://elasticsearch:9200"])

print("DEBUT")


@app.route('/')
def home():
    return render_template('main.html')



@app.route('/search_results', methods=['GET','POST'])
def search_request():
    search_term = request.form["NameInput"]

    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "Titre": search_term
                        }
                    }
                ]
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


