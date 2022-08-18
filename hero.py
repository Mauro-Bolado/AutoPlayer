from telethon import TelegramClient, events, types
from regex import HeroInfo, hero_pattern, test_text
from utils import sessions

api_id = 1267461
api_hash = '168acb04f099beb551aff4069d029320'

class CwClient(TelegramClient, HeroInfo):

    def __init__(self, session, tg=True):
        if tg:
            super().__init__(session=session, api_id = api_id, api_hash = api_hash)

        lp = [k for k in HeroInfo.__dict__.keys() if not k.startswith('__')]
        for item in lp:
            exec(f'self.{item} = None')
            
    def manage_handlers(self, handler_flags: dict):
        try:
            for handler, flag in handler_flags.items():
                pass
            return True
        except Exception as e:
            print("Could not load the handlers correctly")
            return False

    def update(self, me_text: sessions):
        match = hero_pattern.match(me_text)
        if not match:
            print("Error parsing /me")
            return
        dm = match.groupdict()
        lp = [k for k in HeroInfo.__dict__.keys() if not k.startswith('__')]
        for item in lp:
            exec(f'self.{item} = dm[HeroInfo.{item}]')

if __name__ == "__main__":
    a = CwClient(session='kk', tg=False)
    a.update(test_text)
    print(HeroInfo.castle)
    print(a.primary_class)