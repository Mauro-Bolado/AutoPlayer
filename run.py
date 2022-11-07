# coding: utf-8
from email.policy import default
from itertools import count
from telethon import TelegramClient, events, types
from telethon.tl.custom import Message
import asyncio
import logging
from regex import hero_pattern
from hero import CwClient
from handlers import *
from typing import List
import clients
import scriptchats
from datetime import datetime, timedelta, timezone
from telethon.tl.custom import Message
from hero import CwClient
import asyncio
from random import randint
import functools as ft
import re
import types

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s]%(name)s:%(message)s', level=logging.WARNING)

loop = asyncio.get_event_loop()


###########################################################################################
#                                  Events Asignation                                      #
###########################################################################################


clients_list: List[CwClient] = clients.clients()


for client in clients_list:
    client.add_event_handler(me_ping_handler, events.NewMessage(pattern='/ping'))
    client.add_event_handler(go_and_pledge_handler, events.NewMessage(chats='chtwrsbot'))
    client.add_event_handler(autoquest_restored_handler, events.NewMessage(chats='chtwrsbot'))

for client in clients_list:
    client.add_event_handler(go_and_pledge_handler, events.NewMessage(chats='chtwrsbot'))


for client in clients_list:
    client.add_event_handler(auto_click_quest_r_handler, events.NewMessage(chats='@chtwrsbot'))


for client in clients_list:
    client.add_event_handler(massive_spend_handler, events.NewMessage(chats=-1001175888130, pattern=r'/spend (\d{1,2})'))


###########################################################################################
#                                        Orders                                           #
###########################################################################################

class Order:
    attack = ""
    defend = "🛡Defend"
    guild = ""
    guild_alliance = ""
    tactics = ""
    
    def __init__(self, attack = "", guild = "", tactics = "", guild_alliance = ""):
        self.attack = attack
        self.guild = guild
        self.guild_alliance = guild_alliance
        self.tactics = tactics
        
    def __str__(self) -> str:
        if self.guild_alliance != "":
            return self.guild_alliance
        elif self.guild != "":
            return self.guild
        elif self.attack != "":
            return self.attack
        else:
            return self.defend

at_least_one_letter_pattern = re.compile(r'.*[a-zA-Z].*')

async def set_orders_async(client: CwClient, order, pinned=False, func=None):
    now = datetime.now(timezone.utc)
    cw_hour = (now.hour + 1) % 8
    message: Message
    if (now - message.date) > timedelta(hours=cw_hour, minutes=now.minute, seconds=now.second):
        message.raw_text = order
    if func:
        await func(client, message)
    elif message.raw_text != '':
        if at_least_one_letter_pattern.match(message.raw_text):
            await client.send_message('chtwrsbot', message.raw_text)
        else:
            await client.send_message('chtwrsbot', '⚔Attack')
            await asyncio.sleep(randint(3, 6))
            await client.send_message('chtwrsbot', message.raw_text)


def set_orders_sync(client: CwClient, chat, order: str, pinned=False, func=None, minutes=8):
    loop.create_task(set_orders_async(client, chat, order, pinned, func))
    now = datetime.now(timezone.utc)
    cw_hour = (now.hour + 1) % 8
    delta_t = timedelta(hours = 7 - cw_hour, minutes=59 - now.minute, seconds=60 - now.second) \
        - timedelta(minutes=minutes)
    if delta_t.total_seconds() < 0:
        delta_t += timedelta(hours=8)
    delta_s = delta_t.total_seconds()
    loop.call_later(delta_s + randint(30, 250), ft.partial(set_orders_sync, client, chat, order, pinned, func, minutes))


async def set_orders(client: CwClient, chat, order: str, pinned = False, func = None, minutes = 8):
    now = datetime.now(timezone.utc)
    cw_hour = (now.hour + 1) % 8
    delta_t = timedelta(hours=7 - cw_hour, minutes=59 - now.minute, seconds=60 - now.second) \
              - timedelta(minutes=minutes)
    if delta_t.total_seconds() < 0:
        delta_t += timedelta(hours=8)
    delta_s = delta_t.total_seconds()
    loop.call_later(delta_s + randint(30, 250), ft.partial(set_orders_sync, client, chat, order, pinned, func, minutes))
   
test_order = """⚔️🦈
🛡🌑 to DEF!
Tactics: /tactics_sharkteeth (https://t.me/share/url?url=/tactics_sharkteeth)"""

current_order = Order()
default_order = "🛡Defend"

order_pattern = re.compile(r'\W{0,2}'
                           r'(?P<attack>[\S]){0,1}'
                           r'\W+ to DEF!'
                           r'\W+Tactics: \W(?P<tactics>\w+)') 
def castle_order(order: str):
    global current_order
    order_match = re.match(order_pattern, order)
    current_order = Order(order_match.group('attack'), "", order_match.group('tactics'), "") 

async def async_get_castle_order(client: CwClient, sender, event: Message):
    if event.client == client:
        if event.sender is sender:
            castle_order(event.text)
            await set_orders(client, str(current_order), pinned=False, minutes=2)

async def handle():
    for client in clients_list:
        order = await client.get_messages(scriptchats.moon_squad, 1)
        client_event = await async_get_castle_order(client, sender = scriptchats.moon_squad, event = order)
        client.add_event_handler(client_event)

###########################################################################################
#                                        Update Info                                      #
###########################################################################################

text = "🏅Me"

async def up_to_date_info(client: CwClient, message: Message):
    now = datetime.now(timezone.utc)
    cw_hour = (now.hour + 1) % 8
    count = 1
    if cw_hour == 0:
        count = 0
        client.send_message('chtwrsbot', text)
    if cw_hour == 7:
        count = 1
    if message.sender == 'chtwrsbot':
        client.update(message.text)
        file = open('me.txt', 'w')
        file.write(message.text)
        file.close()
        
for client in clients_list:
    client.add_event_handler(up_to_date_info, events.NewMessage(chats='@chtwrsbot'))
    
for client in clients_list:
    client.start()

print("Done")
loop.run_forever()
