import requests, json
from pymongo import MongoClient
def get_hooks():
    p = {"channel": "C1H9RESGL", "blocks": [{"type": "section","text": {"type": "mrkdwn","text": "Danny Torrence left the following review for your property:"}},{"type": "section","block_id": "section567","text": {"type": "mrkdwn","text": "<https://google.com|Overlook Hotel> \n :star: \n Doors had too many axe holes, guest in room 237 was far too rowdy, whole place felt stuck in the 1920s."}}]}
    client = MongoClient("mongodb://localhost:27017")
    database = client["api"]
    collection = database["notifications"]
    payload =json.dumps({"text":"Some problems occured! sorry, try again soon"})
    cursor = collection.find({})
    try:
     for doc in cursor:
       text = (doc['text'])
       apis = [x.strip() for x in text.split(',')] #gets an array for each API name entered by notify me command
       res_url = (doc['response_url'])
       #ELK Request
       if len(apis) >=0:
#         req_url = "http://35.244.98.50:9200/question/so/_search?q=api:"+apis[0]   
         #elk_data = json.dumps({"query":{"bool":{"must":[ {"match":{"api":apis[0]}}]}}})
 #        elk = requests.get(req_url,{})
  #       print(elk, elk.text)
           from elasticsearch import Elasticsearch
           from elasticsearch_dsl import Search
           client = Elasticsearch()
           s = Search(using=client)
           s = s.using(client)
           s = Search().using(client).query("match", api =apis[0])
           response = s.execute()
           msg = "*here are few posts*:\n"
           for hit in s:
               msg = msg + hit.title + '\n' + "<https://stackoverflow.com/questions/"+str(hit.question_id)+"/> \n"
       else:
            msg= "nothing found"

       payload =json.dumps(p)
       r = requests.post(url = res_url, data = payload)
       print(r.text,res_url, payload)
    except KeyError as error:
        print(error)
    return

get_hooks()

