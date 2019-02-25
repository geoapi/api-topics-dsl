from flask import Flask, request, render_template, jsonify
import html
import json, os
import dict
import requests
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

app = Flask(__name__)

#This end point takes json object {"text":"access tokens and facebook and security and returns results from our TDSL and the indexing service"}
@app.route('/tdsl',methods=['GET','POST'])
def getlts():
    import asyncio
    if (request.method == 'POST'):
       content = request.get_json(silent=True)
       txt = content["text"]

       a = dict.check_dsl_string_boolean(txt)
       b = dict.construct_dynamic_dsl_boolean_query(a)
       a = json.loads(b)
       url = 'http://35.244.98.50:9200/question/so/_search'
       
       def make_request(a): 
          r = requests.post('http://35.244.98.50:9200/question/so/_search', json=a)
          return r
       r = make_request(a)
       print(r.json())
       data = r.json()
 #      data = r.text()
    #   noposts = (data['hits']['total'])  # total hits found!
    #   header = 'I found ' + str(noposts) + ' posts, here are few examples: \n'
      # d = {}
    #   post = ''
    #   for i in range(0,3):
    #     title = (data['hits']['hits'][0]['_source']['title'])  # Title
    #     body_sliced = data['hits']['hits'][0]['_source']['body']  # Body
    #     body = (body_sliced[:189])  
       #  link = "https://www.stackoverflow.com/questions/" + str(data['hits']['hits'][0]['_source']['question_id'])
    #     api = data['hits']['hits'][0]['_source']['api']
    #     api = ' '.join(str(x) for x in api)
    #     topic = data['hits']['hits'][0]['_source']['topic'][:10]
    #     topic = " ".join(str(x) for x in topic)
    #     post = post + title +'\n'+ body +'\n'+ '*TOPIC*' + topic +'\n'+ '`API`' + api +'\n'
       return jsonify(data),200

@app.route('/tosal', methods = ['POST', 'GET'])
def tosal():
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
   if (request.method == 'POST'):
     from urllib.parse import parse_qs
     from bson.json_util import dumps
     from bson import json_util
     import datetime
     from ast import literal_eval
     s = request.get_data()
     s = s.decode('utf-8')
     s = parse_qs(s)
    # print(s)
#     res = literal_eval(q.decode('utf8'))
#     print(res)
     user= s["user_id"][0]
     txt = s["text"][0]
     #print(s['text'][0])
     try:
      obj = {
        "date":datetime.datetime.now(),
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
        cursor = collection.find(myquery)
        a = "notfound"
        for doc in cursor:
            if (doc['text']==txt):
                msg = "I've already recorded this notification"
                a = "found"
        if a== "notfound":        
           collection.insert_one(obj)
           msg = "Ok, I have recorded your request and will let you know when we have updates"
    #    if (txt =="delete" or txt =="del"):
    #        collection.remove(myquery)
    #        msg= "I've removed your notification from my records use /notifyme if you changed your mind."
    #    if (txt == "shownotifications" or txt == "shownotif"):
     #       print("check DB connection.")
      #          r = requests.post('https://hooks.slack.com/services/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',d)
       #         msg = "ok"
       # else:
       #     collection.update(myquery,obj,upsert=True)
       #     msg = "Your request is being considered, we'll let you know with updates"
     #     msg = s
     except KeyError as error:
        msg = error
    # return jsonify({"text":json_util.dumps(obj)}),200
   return jsonify({"text":msg}),200

@app.route('/shownotifications',methods=['POST'])
def shownotify():
    import json
    from urllib.parse import parse_qs
    from typing import List, Dict
    if (request.method == 'POST'):
        s = request.get_data()
        s = s.decode('utf-8')
        res = parse_qs(s)
        user= res["user_id"][0]
    #    txt = res["text"][0]
        res_url =res['response_url']
        print(res_url)
        from pymongo import MongoClient
        client = MongoClient("mongodb://localhost:27017")
        database = client["api"]
        collection = database["notifications"]
        myquery = {"user_id":user}
        cursor = collection.find(myquery)
        #d = []
        #r = dict()
        t = ""
        for doc in cursor:
            t= t +"ID: "+(str(doc['_id'])[-4:]+ "  Content:  " + doc["text"])+"\n"
       #TODO text for slack
       
        #if d:
        #    for message in d:
        #        msg = msg + d["text"] + '\n'
        #else:
        #    msg = 'you have not created any notification'
    else:
        return 'bad request',400
    if not t:
        t = "nothing to show!, you can use /notifyme to add new one first"
    return t,200
    #msg

@app.route('/deletenotification',methods=['POST'])
def delnotify():
    from urllib.parse import parse_qs
    from bson.objectid import ObjectId
    from typing import List, Dict
    if (request.method == 'POST'):
        s = request.get_data()
        s = s.decode('utf-8')
        res = parse_qs(s)
        user= res["user_id"][0]
        txt = res["text"][0]
        res_url =res["response_url"][0]
        from pymongo import MongoClient
        client = MongoClient("mongodb://localhost:27017")
        database = client["api"]
        collection = database["notifications"]
        myquery = {"user_id":user}
        cursor = collection.find(myquery)
        got_id =''
        for doc in cursor:
            d_id = doc['_id']
            d_id = str(d_id)
            d_id = d_id[-4:]
            if txt == d_id:
               got_id = doc['_id']
        if got_id:       
            res = collection.delete_one({'_id':got_id})
            result = "Ok, it has been deleted."
        else:
            result = "Can't find it"
        #TODO inspect result and if it's done well return ok if nothing deleted return not found
    return result  

        #TODO text for slack
if __name__  == '__main__':
    app.debug = True
    host = os.environ.get('IP','0.0.0.0')
    port = int(os.environ.get('PORT',7000))
    app.run(host=host,port=port,debug=True)
