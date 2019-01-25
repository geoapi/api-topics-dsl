api_dict = [
             {"name":"facebook","keywords":["facebook graph api", "facebook API", "facebook api", "FB API", "fb api"],"tag":"facebook-graph-api"},
             {"name":"twitter", "keywords":["twitter api", "Twitter API"], "tag":"twitter-api"},
             {"name":"winapi","keywords":["Winapi","win api", "WINAPI", "win32 api", "Windows API","The Windows API"],"tag":"winapi"},
             {"name":"gmail", "keywords":["Google GMail api", "Gmail API"], "tag":"gmail-api"},
             {"name":"java", "keywords":["Java api", "Java API"], "tag":"java-api"},
             {"name": "youtube", "keywords": ["YouTube API"], "tag": "youtube-api"},
             {"name": "googleplaces", "keywords": ["Google Places API"], "tag": "google-places-api"},
             {"name": "instagram", "keywords": ["instagram api","Instagram API"], "tag": "instagram-api"},
              {"name": "youtube", "keywords": ["youtube api"], "tag": "youtube-api"},
             {"name": "", "keywords": [""], "tag": ""},
             {"name": "googlecalendar", "keywords": ["google calendar api"], "tag": "google-calendar-api"},
              {"name": "dropbox", "keywords": ["dropbox api"], "tag": "dropbox-api"},
              {"name": "slack", "keywords": ["slack api"], "tag": "slack-api"},
              {"name": "heresdk", "keywords": ["HERE sdk"], "tag": "here-api"},
             # {"name": "", "keywords": [""], "tag": ""},
             # {"name": "", "keywords": [""], "tag": ""},
             # {"name": "", "keywords": [""], "tag": ""},
             # {"name": "", "keywords": [""], "tag": ""},
             # {"name": "", "keywords": [""], "tag": ""},
             # {"name": "", "keywords": [""], "tag": ""},
             # {"name": "", "keywords": [""], "tag": ""},
             # {"name": "", "keywords": [""], "tag": ""},
             # {"name": "", "keywords": [""], "tag": ""},
             # {"name": "", "keywords": [""], "tag": ""},
             # {"name": "", "keywords": [""], "tag": ""},
             # {"name": "", "keywords": [""], "tag": ""},
             # {"name": "", "keywords": [""], "tag": ""},
             # {"name": "", "keywords": [""], "tag": ""},
            ]

topic_dict = [
    {"id":0,"name":"API security","category_id":0, "keywords":["security"]},
    {"id":1,"name":"oauth configuration","category_id":0,"keywords":["oauth","authentication","configuration","settings"]},
    {"id":2,"name":"oauth clarification","category_id":0,"keywords":["oauth"]}, #,"understand","clarify" take out as they are not necessarly related to oauth
    {"id":3,"name":"api constraints","category_id":1,"keywords":["restrictions"]},
    {"id":4,"name":"possibility of a functionality","category_id":1,"keywords":["possible","feasible","doable"]},
    {"id":5,"name":"understanding usage limitation","category_id":1,"keywords":["limited","restricted","impossible"]},
    {"id":6,"name":"debugging","category_id":2,"keywords":["debug","fix","error","bug"]},
    {"id":7,"name":"request","category_id":2,"keywords":["request","call","invocation"]},
    {"id":8,"name":"behaviour","category_id":2,"keywords":["behaviour"]},
    {"id":9,"name":"parameters","category_id":2,"keywords":["param","parameter"]},
    {"id":10,"name":"returned data","category_id":2,"keywords":["returned","requested","data"]},
    {"id":11,"name":"settings","category_id":3,"keywords":["settings","configuration"]},
    {"id":12,"name":"usage","category_id":4,"keywords":["usage","use","example"]},
    #{"id":13,"name":"features implementation feasibility","category_id":4,"parent":false,"keywords":["feature","feasible","possible"]},
    {"id":14,"name":"understanding functionality","category_id":4,"keywords":["how to","need to","know"]},
    {"id":15,"name":"seeking alternative implementation","category_id":4,"keywords":["alternative","way","another"]},
    {"id":16,"name":"development environment","category_id":4,"keywords":["environment","development","development-mode"]},
    {"id":17,"name":"examples","category_id":4,"keywords":["example","code"]},
    {"id":18,"name":"documentation","category_id":5,"keywords":["documentation","docs","reference"]},
    {"id":19,"name":"redirection","category_id":5,"keywords":["redirect"]},
    {"id":20,"name":"reporting issues","category_id":5,"keywords":["typo","mistake","error"]},
    {"id":21,"name":"definition","category_id":6,"keywords":["definition"]},
    {"id":22,"name":"design patterns","category_id":6,"keywords":["design","design-pattern","design-patterns"]},
    {"id":23,"name":"version management","category_id":6,"keywords":["version"]},
    {"id":24,"name":"setting parameters","category_id":6,"keywords":["setting","parameter"]},
    {"id":25,"name":"recommendation","category_id":6,"keywords":["recommend"]}
    ]

def check_bdsl_string(dsl_string):
    print(dsl_string)
    dsl_string = dsl_string.encode('utf-8')
    print(dsl_string)
    dsl_string = dsl_string.split(' ')
    #prepare a bare-list of api names and another for topic names so we can match
    topic_dict_temp = []
    api_dict_temp = []
    topic_name = []
    api_name = []
    for item in api_dict:
        if item['name']:
          api_dict_temp.append(item['name'])
        for key in item['keywords']:
           if key:
               api_dict_temp.append(key)
    topics_dict_temp = []
    for item in topic_dict:
        topics_dict_temp.append(item['name'])
        for key in item['keywords']:
            if key:
                topics_dict_temp.append(key)
    not_included_dict = []
    for one_item in dsl_string:
        user_keyword = ''.join(filter(str.isalnum,one_item))
        operator = one_item[0]
        if (user_keyword in topics_dict_temp and operator == '/'):
            topic_name.append(user_keyword)
        if (user_keyword in api_dict_temp and operator == '/'):
            api_name.append(user_keyword)
        if (operator == '-'):
            not_included_dict.append(user_keyword)

    return(topic_name,api_name,not_included_dict)
# Dynamic Construction of ELK DSL
def construct_dynamic_dsl(topic_name,api_name,not_included_dict):
    i = 0
    op = ''
    match_ = ''
    while (len(topic_name) >= 1 and i < len(topic_name)):
       match_ = match_ +op+' {"match":{"topic":"'+topic_name[i]+'"}}'
       op = ','
       i +=1
    i = 0
    while (len(api_name) >= 1 and i < len(api_name)):
        match_ = match_ + op + ' {"match":{"api":"' + api_name[i] + '"}}'
        op = ','
        i += 1
    if (len(topic_name) >1 or len(api_name) > 1):
        match_ = '{"bool": {"must": ['+match_+']}}'
# MUST NOT
    i = 0
    op = ''
    match2_ = ''
    while (len(not_included_dict) >= 1 and i < len(not_included_dict)):
        match2_ = match2_ + op + ' {"match":{"tags":"' + not_included_dict[i] + '"}}'
        op = ','
        i += 1
    if not_included_dict:
        match2_ = ',{"bool":{"must_not":['+match2_+']}}'
    dsl = '{"query":{"bool":{"must":['+match_+match2_+']}}}'
    return dsl


