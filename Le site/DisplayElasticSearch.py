from flask import Flask, render_template,request
from elasticsearch import Elasticsearch

app = Flask(__name__)

es_client = Elasticsearch(hosts=["http://localhost:9200"])

@app.route('/')
def home():
    return render_template('main.html')



@app.route('/search_results', methods=['GET','POST'])
def search_request():
    print(request.method)
    search_term = request.form["NameInput"]
    print(search_term)

    body = {
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
    res = es_client.search(
        index="job_offer",
        size=20,
        body=body)

    return render_template('search_results.html', res=res)

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='0.0.0.0', port=5000,debug = True)


