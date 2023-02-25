from elasticsearch.helpers import scan
from flask import Flask, render_template,request
from elasticsearch import Elasticsearch
import pandas as pd

class app_es:
    def __init__(self,elastic_client):
        self.es_client = elastic_client


app = Flask(__name__)
print("DEBUT")

#Page principale, celle qui est affichée quand on ouvre le site
@app.route('/')
def home():
    return render_template('main.html')


#Page "Search results", qui se lance quand on clique sur le bouton rechercher un stage
@app.route('/search_results', methods=['GET','POST'])
def search_request():

        #Récupération de toutes les requêtes (Nom du stage, type de contrat, etc)
        search_term = request.form["NameInput"]
        contrat_term = request.form["ContratInput"]
        bac_req = request.form['bac_select']
        duration_req = request.form['duration_select']

        #On compte le nombre de termes remplis (l'utilisateur peut choisir de ne pas renseigné une durée de stage par exemple)
        counter_term=0
        if search_term !="":
            counter_term +=1
        if contrat_term !="":
            counter_term +=1
        if bac_req!='0':
            counter_term +=1
        if duration_req !='0':
            counter_term +=1



        #On effectue la query sur elastic search. On demande a la Query d'avoir autant de termes qui "match" que de nombre de termes remplis, calculé précédement
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
        rel = scan(client=app_es.es_client,
                       query=query,
                       scroll='1m',
                       index='job_offer',
                       raise_on_error=True,
                       preserve_order=False,
                       clear_scroll=True
                       )
        #On met dans une liste les résultat, puis on les retourne a la page web. Le reste se fera dans le code HTML de "search_results.html"
        result = list(rel)

        return render_template('search_results.html', res=result)

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='0.0.0.0')


