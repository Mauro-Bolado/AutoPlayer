from hero import CwClient, events, TelegramClient
from utils import sessions
from telethon.sessions import StringSession
from typing import List

api_id = 1267461
api_hash = '168acb04f099beb551aff4069d029320'

def clients():
   result :List[CwClient] = [v for (k, v) in globals().items() if type(v) == CwClient]
   return result

artorias = CwClient(session = StringSession(sessions.artorias), tg = True)
