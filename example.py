from flask import Flask, request, render_template
import json
import dict
app = Flask(__name__)
@app.route('/tosal', methods = ['POST', 'GET'])
def hello_world():
    if request.method == 'GET':
        return render_template('basic_form.html')
    elif request.method == 'POST':
        data = {
            "query": request.form['query'],
            "submit_value":request.form['submit']
        }
        query = (data["query"])
        a = dict.check_bdsl_string(query)
        b = dict.construct_dynamic_dsl(a[0],a[1],a[2],a[3])
        return render_template('results.html',data =b)


@app.route('/dsl', methods = ['POST', 'GET'])
def get_dsl():
    if request.method == 'GET':
        return render_template('basic_form.html')
    elif request.method == 'POST':
        return render_template('results.html',data)


@app.route('/', methods = ['POST', 'GET'])
def hello_dsl():
    if request.method == 'GET':
        return render_template('dsl_form.html')
    elif request.method == 'POST':
        data = {
            "query": request.form['query'],
            "submit_value":request.form['submit']
        }
        query = (data["query"])
        cql = dict.check_dsl_string_boolean(query)
        dsl = dict.construct_dynamic_dsl_boolean_query(cql)
        return render_template('dsl_results.html',data =dsl)

@app.route('/apis',methods=['GET'])
def get_apis():
  if request.method =='GET':
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    database = client["api"]
    collection = database["api"]
    query = {}
    d = {}
    cursor = collection.find(query)
    try:
        for doc in cursor:            
            d["name"]=doc['name']
        finally:
            client.close()
    return jsonify(d)

