import requests,dict,json, html
content = {"text":"access tokens and security and facebook"}
print(content['text'])
txt = content["text"]
# GET THE TEXT FROM RIVESCRIPT
# Convert the text into a TDSL
a = dict.check_dsl_string_boolean(txt)
# print(a)
b = dict.construct_dynamic_dsl_boolean_query(a)

a = json.loads(b)

# now we have json body for a request to make for the search
r = requests.post('http://35.244.98.50:9200/question/so/_search', json=a)
# print(r.status_code,r.json())
data = r.json()
noposts = (data['hits']['total'])  # total hits found!
title = "I found " + str(noposts) + " number of posts, here are few examples:"
d = {}
d['text'] = title
attach = []
for i in range(0, 3):
    title = (data['hits']['hits'][i]['_source']['title'])  # Title
    body_sliced = data['hits']['hits'][i]['_source']['body']  # Body
    #body = (html.escape(body_sliced[:200])) # sliced body and escpaed from special chars then converted to string .encode('ascii', 'xmlcharrefreplace')).decode("utf-8")
    body = (body_sliced[:200])  # sliced body and escpaed from special chars then converted to string .encode('ascii', 'xmlcharrefreplace')).decode("utf-8")

    p = {}
    # body_sliced = data[:200]
    link = "https://www.stackoverflow.com/questions/" + str(data['hits']['hits'][i]['_source']['question_id'])
    # print(link)
    api = data['hits']['hits'][i]['_source']['api']
    api = " ".join(str(x) for x in api)
    # print(api)
    topic = data['hits']['hits'][i]['_source']['topic'][:10]
    topic = " ".join(str(x) for x in topic)
    #post = '{"type": "section","text":"*' + title + body + '<' + link + '> ' + '` TOPIC `' + topic + '` API `' + api + '"}'
    p['text'] = "*"+ title + "*\n" + body + "\n" + link +"\n" + " `API` \n "+api +"\n" + " `TOPIC`"+" \n "+topic
    attach.append(p)
d['attachments']= attach
#print(attach_me)
j=json.dumps(d)
r = requests.post('https://hooks.slack.com/services/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',j)
print(r.status_code)

# import json, requests
# noposts = 45

# title = "some title"
# body = "epsumepsume ps umeps umepsum e psumep sum"
# link = "http://link.com"
#
# apis = "api1, api2"
# topics = "Topic1 , T2, T3"
#
#
# head_section = '{"text": "I found '+ str(noposts) + ' number of posts, here are few examples:","attachments":['
# posts = ""
# op=""
# for i in range(0, 3):
#   post = '{"type": "section","text":"*'+ title +'*\\n' + body + '\\n' + '<' + link + '>\\n' + '` TOPIC `' + topics +  ' ` API `'+ apis + '"}'
#   posts = posts  + op + post
#   if i != 3:
#       op =','
#   else:
#       op = ''
# attach_me = head_section  + posts + ']}'
#             #+ ',' + actions_buttons
# print(attach_me)
# r = requests.post('https://hooks.slack.com/services/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', json=json.loads(attach_me)  )
# print(r.status_code)