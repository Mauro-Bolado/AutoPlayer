from hero import CwClient, events, TelegramClient
from utils import sessions
from telethon.sessions import StringSession
from typing import List


def clients():
   result :List[CwClient] = [v for (k, v) in globals().items() if type(v) == CwClient]
   return result

artorias = CwClient(session = StringSession(sessions.artorias), tg = True)
