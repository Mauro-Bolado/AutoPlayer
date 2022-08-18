from http import client
from telethon import TelegramClient
from telethon.sessions import StringSession

api_id = 1267461
api_hash = '168acb04f099beb551aff4069d029320'
    
def save_session(client, str_session):
   file = open("utils/sessions.py", "a")
   str = client + ' = "' + str_session + '"'
   file.write('\n' + str)
   file.close()
   
   file = open("clients.py", "a")
   str = client + ' = CwClient(session=sessions.' + client + ', tg=True)'
   file.write('\n' + str)
   file.close()

with TelegramClient(StringSession(), api_id, api_hash) as session:
    client = input("Enter your client: ")
    str = session.session.save()
    save_session(client, str)