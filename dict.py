from collections import deque
from apitopicsdict import topic_dict,api_dict
def check_bdsl_string(dsl_string):
   # print(dsl_string)
    dsl_string = dsl_string.encode('utf-8')
  #  print(dsl_string)
    dsl_string = dsl_string.decode().split(' ')#locally
#    dsl_string = dsl_string.split(' ') #on deployment!!!
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
    not_included_dict_topics = []
    not_included_dict_apis = []
    for one_item in dsl_string:
        user_keyword = ''.join(filter(str.isalnum,one_item))
        operator = one_item[0]
        if (user_keyword in topics_dict_temp and operator == '/'):
            topic_name.append(user_keyword)
        if (user_keyword in api_dict_temp and operator == '/'):
            api_name.append(user_keyword)
        if (user_keyword in topics_dict_temp and operator == '-'):
            not_included_dict_topics.append(user_keyword)
        if (user_keyword in api_dict_temp and operator == '-'):
            not_included_dict_apis.append(user_keyword)

    return(topic_name,api_name,not_included_dict_topics,not_included_dict_apis)
# Dynamic Construction of ELK DSL
def construct_dynamic_dsl(topic_name,api_name,not_included_dict_topics,not_included_dict_apis):
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
# MUST NOT for api topics
    i = 0
    op = ''
    match2_ = ''
    while (len(not_included_dict_topics) >= 1 and i < len(not_included_dict_topics)):
        match2_ = match2_ + op + ' {"match":{"topic":"' + not_included_dict_topics[i] + '"}}'
        op = ','
        i += 1

# MUST NOT for APIs
    i = 0
    op = ''
    match3_ = ''
    while (len(not_included_dict_apis) >= 1 and i < len(not_included_dict_apis)):
        match3_ = match3_ + op + ' {"match":{"api":"' + not_included_dict_apis[i] + '"}}'
        op = ','
        i += 1

    if not_included_dict_topics and not_included_dict_apis:
        match2_ = ',{"bool":{"must_not":['+match2_+match3_+']}}'
    elif not_included_dict_topics:
        match2_ = ',{"bool":{"must_not":[' + match2_ + ']}}'
    elif not_included_dict_apis:
        match2_ = ',{"bool":{"must_not":[' + match3_ + ']}}'

    dsl = '{"query":{"bool":{"must":['+match_+match2_+']}}}'
    return dsl


def check_dsl_string_boolean(dsl_string):
   # print(dsl_string)
  #  dsl_string = dsl_string.encode('utf-8')
  #  print(dsl_string)
#    dsl_string = dsl_string.decode().split(' ')#locally
    op = ["AND","OR","and","or","And","Or"]
    dsl_string = dsl_string.lower()
    dsl_string = dsl_string.split(' ') #on deployment!!!
    #prepare a bare-list of api names and another for topic names so we can match
    query = ""
  #  topic_dict_temp = []
    api_dict_temp = []
    topic_name_and = []
    api_name_and = []

    api_name_or = []
    topic_name_or = []

    api_name_not = []
    topic_name_not = []


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
    #not_included_dict_topics = []
    #not_included_dict_apis = []
    collect_query_op = []
    l = deque(dsl_string)

    #HAVE THE QUERY SEPERATED AND COLLECTED AS A SENTENCE

    while (len(l) > 0 and l[0] not in op) :
        query = query + " " + l.popleft()
    collect_query_op.append(query)

    while (len(l) > 0):
        query = ""
        getOp = l.popleft()
        getKey = l.popleft()
        if getOp == "AND" or getOp == "And" or getOp == "and":
            if (getKey in api_dict_temp):
                api_name_and.append(getKey)
            elif (getKey in topics_dict_temp):
                topic_name_and.append(getKey)
        elif getOp == "OR" or getOp == "Or" or getOp == "or" :
            if (getKey in api_dict_temp):
                api_name_or.append(getKey)
            elif (getKey in topics_dict_temp):
                topic_name_or.append(getKey)
        elif getOp == "NOT" or getOp == "Not" or getOp == "not":
            if (getKey in api_dict_temp):
                api_name_not.append(getKey)
            elif (getKey in topics_dict_temp):
                topic_name_not.append(getKey)
    collect_query_op.append(api_name_and)
    collect_query_op.append(topic_name_and)
    collect_query_op.append(api_name_or)
    collect_query_op.append(topic_name_or)
    collect_query_op.append(api_name_not)
    collect_query_op.append(topic_name_not)
    print(collect_query_op)
       # while (len(l) > 0 and l[0] not in op):
        #    query = query + " " + l.popleft()
    #collect_query_op.append(query)

    #print(collect_query_op)
    #process_list = deque(collect_query_op)
    #op_chk = ['/','+','-']
    #while (len(process_list) > 0):
    #    elem = process_list.popleft()
    #    if elem[0] in op_chk:
    #        body = elem
    #    else:
    #         q = ''.join(filter(str.isalnum,one_item))
    #         operator = process_list[0]
    #     if (process_list in topics_dict_temp and operator == '/'):
    #         print('ok')
    #     #     topic_name.append(user_keyword)
        # if (user_keyword in api_dict_temp and operator == '/'):
        #     api_name.append(user_keyword)
        # if (user_keyword in topics_dict_temp and operator == '-'):
        #     not_included_dict_topics.append(user_keyword)
        # if (user_keyword in api_dict_temp and operator == '-'):
        #     not_included_dict_apis.append(user_keyword)
        #return
     #The list contains these elements in order
     #(query, API ANDs, TOPIC ANDS, API OR, TOPIC OR, API NOT, TOPIC NOT) the AND with API means list of APIs that need to be treated with AND op .. lists may be empty
    return (collect_query_op)

def construct_dynamic_dsl_boolean_query(obj):
    obj = deque(obj)
    query = obj.popleft()
    api_anded = obj.popleft()
    topic_anded = obj.popleft()
    api_or = obj.popleft()
    topic_or = obj.popleft()
    api_not = obj.popleft()
    topic_not = obj.popleft()
    match_ = ''

    if (len(query) >= 1):
       match_ = ' {"match":{"body":"'+query+'"}}'
    i = 0
    op =','
    while (len(api_anded) >= 1 and i < len(api_anded)):
        match_ = match_ + op + ' {"match":{"api":"' + api_anded[i] + '"}}'
        op = ','
        i += 1
    i = 0
    if len(topic_anded) >=1:
        op = ','
    else:
        op = ''
    while (len(topic_anded) >= 1 and i < len(topic_anded)):
        match_ = match_ + op + ' {"match":{"topic":"' + topic_anded[i] + '"}}'
        op = ','
        i += 1

    if (len(api_anded) >1 or len(topic_anded) > 1):
        match_ = '{"bool": {"must": ['+match_+']}}'

# MUST NOT for apis
    i = 0
    op = ''
    match2_ = ''
    while (len(api_not) >= 1 and i < len(api_not)):
        match2_ = match2_ + op + ' {"match":{"api":"' + api_not[i] + '"}}'
        op = ','
        i += 1

# MUST NOT for APIs
    i = 0
    op = ''
    match3_ = ''
    while (len(topic_not) >= 1 and i < len(topic_not)):
        match3_ = match3_ + op + ' {"match":{"topic":"' + topic_not[i] + '"}}'
        op = ','
        i += 1
# API OR
    i = 0
    op = ''
    match4_ = ''
    while (len(api_or) >= 1 and i < len(api_or)):
        match4_ = match4_ + op + ' {"match":{"api":"' + api_or[i] + '"}}'
        op = ','
        i += 1

# TOPIC OR
    i = 0
    op = ''
    match5_ = ''
    while (len(topic_or) >= 1 and i < len(topic_or)):
        match5_ = match5_ + op + ' {"match":{"topic":"' + topic_or[i] + '"}}'
        op = ','
        i += 1

    if topic_not and api_not:
        match2_ = ',{"bool":{"must_not":['+match2_+','+match3_+']}}'
    elif topic_not:
        match2_ = ',{"bool":{"must_not":[' + match3_ + ']}}'
    elif api_not:
        match2_ = ',{"bool":{"must_not":[' + match2_ + ']}}'

    if api_or and topic_or:
        match6_ = ',{"bool":{"should":['+match4_+match5_+']}}'
    elif topic_or:
        match6_ = ',{"bool":{"should":[' + match5_ + ']}}'
    elif api_or:
        match6_ = ',{"bool":{"should":[' + match4_ + ']}}'
    else:
        match6_ =''

    dsl = '{"query":{"bool":{"must":['+match_+match2_+match6_+']}}}'
    return dsl


#cql = check_dsl_string_boolean("short term AND facebook AND security AND oauth NOT debugging")
#dsl = construct_dynamic_dsl_boolean_query(cql)
#print(dsl)

#a = check_bdsl_string('/facebook /security -debugging -here_api')
#b = construct_dynamic_dsl(a[0],a[1],a[2],a[3])
#print(b)

