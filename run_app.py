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

@app.route('/test', methods = ['POST', 'GET'])
def tosa22l():
    if request.method == 'GET':
        return 'hello geo'
    elif request.method == 'POST':
        return 'render_templatdata =b)'

#This end point takes json object {"text":"access tokens and facebook and security and returns results from our TDSL and the indexing service"}
@app.route('/tdsl',methods=['GET','POST'])
def getlts():
    if (request.method == 'POST'):
       content = request.get_json(silent=True)
       print(content['text'])
       txt = content["text"]

       a = dict.check_dsl_string_boolean(txt)
       # print(a)
       b = dict.construct_dynamic_dsl_boolean_query(a)

       a = json.loads(b)

       # now we have json body for a request to make for the search
       r = requests.post('http://35.244.98.50:9200/question/so/_search', json=a)
       # print(r.status_code,r.json())
       data = r.json()
       noposts = (data['hits']['total'])  # total hits found!
       head_section = '{"text": "I found ' + str(noposts) + ' number of posts, here are few examples:","attachments":['
       posts = ''
       op = ''
       for i in range(0, 3):
           title = (data['hits']['hits'][i]['_source']['title'])  # Title
           body_sliced = data['hits']['hits'][i]['_source']['body']  # Body
           body = body_sliced[:200]  # sliced body and escpaed from special chars then converted to string .encode('ascii', 'xmlcharrefreplace')).decode("utf-8")

           # body_sliced = data[:200]
           link = "https://www.stackoverflow.com/questions/" + str(data['hits']['hits'][i]['_source']['question_id'])
           # print(link)

           api = data['hits']['hits'][i]['_source']['api']
           api = " ".join(str(x) for x in api)
           # print(api)
           topic = data['hits']['hits'][i]['_source']['topic'][:10]
           topic = " ".join(str(x) for x in topic)
           # post = '{"type": "section","text":"*' + title + body + '<' + link + '> ' + '` TOPIC `' + topic + '` API `' + api + '"}'
           #post = '{"text":"*' + title + '*\n' + "body" + '\n' + '<' + link + '>\n' + '` TOPIC `' + topic + ' ` API `' + api + '"}'
           post = {"text":'"' + title  + body + link + '` TOPIC `' + topic + '` API `' + api+'"'}
           posts = posts + op + json.dumps(post)
           if i != 3:
               op = ','
           else:
               op = ''
       attach_me = head_section + posts + ']}'
       # + ',' + actions_buttons
       print(attach_me)
       #
       #asp = json.dumps(attach_me)
       #asp = asp.cgi.escape()
       r = requests.post('https://hooks.slack.com/services/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',attach_me)
       print(r.status_code)
    return  'ok',200


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
   if (request.method == 'POST'):
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
    
