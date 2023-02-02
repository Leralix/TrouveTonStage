from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

app = Flask(__name__)

es_client = Elasticsearch(hosts=["http://localhost:9200"])

@app.route('/')
def home():
    return render_template('search.html')


def checkbox_button():
    s=""
    if request.form.get('bac+3'):
        s+="bac+3 "
    if request.form.get('bac+4'):
        s+="bac+4 "
    if request.form.get('bac+5'):
        s+="bac+5 "
    return s.strip()


@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]

    search_checkbox = checkbox_button()

    if search_checkbox == "":
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
    else:
        body = {
    "query": {
    "bool": {
      "must": [
        {
          "match": {
            "BacFormat": {
              "query" : search_checkbox,
              "operator":"and"
                          }
          }
        },
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




        body = body)

    return render_template('results.html', res=res )

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='0.0.0.0', port=5000)


"""body={
            "query": {
                "multi_match" : {
                    "query": search_term,
                    "fields": [
                        "Titre",
                        "BacFormat"
                    ]
                }
            }
        })"""