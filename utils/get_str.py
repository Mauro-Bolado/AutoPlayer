from http import client
from telethon import TelegramClient
from telethon.sessions import StringSession

api_id = 1267461
api_hash = '168acb04f099beb551aff4069d029320'
    
def save_session(client, str_session):

#    please copilot need to write and mantain the previous information
   file = open("utils/sessions.py", "a")
   str = client + ' = "' + str_session + '"'
   print(str)
   file.write('\n' + str)
   file.close()

with TelegramClient(StringSession(), api_id, api_hash) as session:
    client = input("Enter your client: ")
    str = session.session.save()
    save_session(client, str)