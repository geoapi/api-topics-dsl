from flask import Flask, request, render_template, jsonify
import json, os
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
    d = [] 
    cursor = collection.find(query)
    for doc in cursor:
       d.append(doc['name'])
 #   client.close()
    return jsonify({'name':d})

if __name__  == '__main__':
    app.debug = True
    host = os.environ.get('IP','0.0.0.0')
    port = int(os.environ.get('PORT',7000))
    app.run(host=host,port=port)

@app.route('/topics',methods=['GET'])
def get_topics():
  if request.method =='GET':
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    database = client["api"]
    collection = database["topics"]
    query = {}
    d = []
    cursor = collection.find(query)
    try:
     for doc in cursor:
       d.append(doc['name'])
    except:
        print("No hosts found")   
    return jsonify({'name':d})

@app.route('/tagged_posts',methods=['GET'])
def get_posts():
  if request.method =='GET':
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    database = client["api"]
    collection = database["questions"]
    query = { "tags": { "$in": ["facebook-api","facebook-graph-api"] } }
    d = []
    cursor = collection.find(query)
    try:
     for doc in cursor:
       d.append(doc['title'])
    except:
        print(" error found")
    return jsonify({'items':d})

@app.route('/search')
def search_posts():
    api = request.args.get("api")
    q = request.args.get("q")
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    database = client["api"]
    collection = database["questions"]
    query = {"$match":{"$and":[{"body":"/.*"+q+".*/i"},{"api":api}]}}
    cursor = collection.aggregate([query])
    d=[]
    try:
        for doc in cursor:
            d.append(doc['title'])
    except:
        print("check DB connection.")
    return jsonify({"api_q":d})
#db.questions.aggregate([{$match:{$and:[{body:/.*limitation.*/i},{api:"facebook"}]}}]);

@app.route('/notifyme',methods=['GET','POST'])
def notifyme():
     # msg = 'ready'
     # if (request.method == 'POST'):
     from urlparse import parse_qs
     from bson.json_util import dumps
     from bson import json_util
     s = request.get_data()
     s = parse_qs(s)
     user= s["user_id"][0]
     txt = s["text"][0]
     #print(s['text'][0])
     try:
      obj = {
        "token": s["token"][0],
        "team_id": s["team_id"][0],
        "team_domain":s["team_domain"][0],
        "channel_id":s["channel_id"][0],
        "channel_name":s["channel_name"][0],
        "user_id":s["user_id"][0],
        "user_name":s["user_name"][0],
        "command":s["command"][0],
        "text":s["text"][0],
        "response_url":s["response_url"][0],
        "trigger_id":s["trigger_id"][0]
            }
     except KeyError as error:
            msg = error
     #print(obj)       
     try:
        from pymongo import MongoClient
        client = MongoClient("mongodb://localhost:27017")
        database = client["api"]
        collection = database["notifications"]
        myquery = {"user_id":user}
        #collection.insert_one(obj)
        if (txt =="delete" or txt =="del"):
            collection.remove(myquery)
            msg= "I've removed your notification from my records use /notifyme if you changed your mind."
        else:    
            collection.update(myquery,obj,upsert=True)
            msg = "Your request is being considered, we'll let you know with updates"
     #     msg = s
     except KeyError as error:
        msg = error       
    # return jsonify({"text":json_util.dumps(obj)}),200
     return jsonify({"text":msg}),200

if __name__  == '__main__':
    app.debug = True
    host = os.environ.get('IP','0.0.0.0')
    port = int(os.environ.get('PORT',7000))
    app.run(host=host,port=port,debug=True)
    
