#This example simplify the Dynamic JSON Creation for posts to be sent to Slack
import json
title = "some tiles on my head! /n \n"
data = {}
data['title'] = title

attach = []
for i in range(0,3):
    p = {}
    p['title'] = title
    attach.append(p)
data['attachments']= attach
print(data)
print(json.dumps(data))



# {
#     "text": "Would you like to play a game?",
#     "attachments": [
#         {
#             "text": "Choose a game to play",
#             "fallback": "You are unable to choose a game",
#             "callback_id": "wopr_game",
#             "color": "#3AA3E3",
#             "attachment_type": "default",
#             "actions": [
#                 {
#                     "name": "game",
#                     "text": "Chess",
#                     "type": "button",
#                     "value": "chess"
#                 },
#                 {
#                     "name": "game",
#                     "text": "Falken's Maze",
#                     "type": "button",
#                     "value": "maze"
#                 },
#                 {
#                     "name": "game",
#                     "text": "Thermonuclear War",
#                     "style": "danger",
#                     "type": "button",
#                     "value": "war",
#                     "confirm": {
#                         "title": "Are you sure?",
#                         "text": "Wouldn't you prefer a good game of chess?",
#                         "ok_text": "Yes",
#                         "dismiss_text": "No"
#                     }
#                 }
#             ]
#         }
#     ]
# }