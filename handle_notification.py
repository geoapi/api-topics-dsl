import requests,dict,json,dict
from urllib.parse import parse_qs
from typing import List, Dict
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
database = client["api"]
collection = database["notifications"]
cursor = collection.find({})
for doc in cursor:
    #print(doc['_id'])
    txt = (doc['text'])
    res_url = (doc['response_url'])
    a = dict.check_dsl_string_boolean(txt)
    b = dict.construct_dynamic_dsl_boolean_query(a)
    a = json.loads(b)
    r = requests.post('http://35.244.98.50:9200/question/so/_search', json=a)
    data = r.json()
    noposts = (data['hits']['total'])
    title_header = "I found " + str(noposts) + " posts, here are few:"
    posts =''
    if noposts == 0:
        attach_me ='nothing found'
    elif noposts > 3:
        k =3
    else:
        k=noposts
    for i in range(0, 3):
        title = (data['hits']['hits'][i]['_source']['title'])
        body = (data['hits']['hits'][i]['_source']['body'])[:200] # Body
        link = "stackoverflow.com/questions/" + str(data['hits']['hits'][i]['_source']['question_id'])
        api = data['hits']['hits'][i]['_source']['api']
        api = " ".join(str(x) for x in api)
        topic = data['hits']['hits'][i]['_source']['topic'][:10]
        topic = " ".join(str(x) for x in topic)
        posts = posts + '\n *'+ title + '* \n' + body + '\n'+ link + '\n' + ' ` TOPIC ` ' + topic + '\n'+ ' ` API ` ' + api + '\n' + '\n'
    attach_me = title_header +posts
    print(res_url, attach_me)
    r = requests.post(res_url,json.dumps({'text':attach_me}))
    print(r)

