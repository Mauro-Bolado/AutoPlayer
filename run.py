# coding: utf-8
from telethon import TelegramClient, events, types
from telethon.tl.custom import Message
import asyncio
import logging
import re
from random import randint
from datetime import datetime, timedelta, timezone
from regex import hero_pattern
from hero import CwClient
from handlers import *
from typing import List
import functools as ft
from utils import sessions
import clients

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s]%(name)s:%(message)s', level=logging.WARNING)

loop = asyncio.get_event_loop()


###########################################################################################
#                                  Asignando Eventos
###########################################################################################


clientes: List[CwClient] = [v for (k, v) in globals().items() if type(v) is CwClient]

for client in clientes:
    # print(client.__repr__())
    client.add_event_handler(me_ping_handler, events.NewMessage(chats='me', pattern='/ping'))
    # client.add_event_handler(go_and_pledge_handler, events.NewMessage(chats='chtwrsbot'))


# migue.add_event_handler(me_ping_handler, events.NewMessage(chats='me', pattern='/ping'))

# #oracle, ephi
for client in clients:
    client.add_event_handler(autoquest_restored_handler, events.NewMessage(chats='@chtwrsbot'))

#oracle, ephi
for client in clients:
    client.add_event_handler(auto_click_quest_1_handler, events.NewMessage(chats='@chtwrsbot'))

#oracle, ephi
for client in clients:
    client.add_event_handler(massive_spend_handler, events.NewMessage(chats='me', pattern=r'/spend (\d{1,2})'))


###########################################################################################
#                                        Set Orders
###########################################################################################

at_least_one_letter_pattern = re.compile(r'.*[a-zA-Z].*')

async def set_orders_async(client: CwClient, chat, order, pinned=False, func=None):
    now = datetime.now(timezone.utc)
    cw_hour = (now.hour + 1) % 8
    message: Message
    if pinned:
        message = await client.get_messages(chat, ids=types.InputMessagePinned())
    else:
        async for message in client.iter_messages(chat, 1):
            pass
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
    delta_t = timedelta(hours=7 - cw_hour, minutes=59 - now.minute, seconds=60 - now.second) \
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
    # if client == yeyo:
    #     print(delta_t)
    loop.call_later(delta_s + randint(30, 250), ft.partial(set_orders_sync, client, chat, order, pinned, func, minutes))


for client in []:
    loop.create_task(set_orders(client, chat=scriptchats.defenders, order='/ga_def', minutes=50))

loop.run_forever()

