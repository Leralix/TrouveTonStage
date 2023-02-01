from flask import Flask, render_template
from elasticsearch import Elasticsearch

app = Flask(__name__)


es_client = Elasticsearch(hosts=["http://localhost:9200"])

@app.route('/')
def home():
    return render_template('index.html')



if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='0.0.0.0', port=5000,debug = True)


