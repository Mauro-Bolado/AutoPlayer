from enum import Enum
from re import compile


class HeroInfo():
    castle_emoji = 'castle_emoji'
    guild_emoji = 'guild_emoji'
    name = 'name'
    guild_tag = 'guild_tag'
    primary_class = 'primary_class'
    castle = 'castle'
    level = 'level'
    total_atk = 'atk'
    total_def = 'def'
    exp = 'exp'
    hp = 'hp'
    stamina = 'stamina'
    max_stamina = 'max_stamina'
    mana = 'mana'
    pogs = 'pogs'
    diamonds = 'diamonds'
    eq_atk = 'eq_atk'
    eq_def = 'eq_def'
    pet_emoji = 'pet_emoji'
    pet_name = 'pet_name'
    pet = 'pet'
    pet_level = 'pet_level'
    pet_status = 'pet_status'
    state = 'state'


test_text = """🌟Congratulations! New level!🌟
Press /level_up

Battle of the seven castles in 2h 1 minutes!

🌑[KGM]Artorias Alchemist of Moonlight Castle
🏅Level: 74 35.87%
⚔️Atk: 802 🛡Def: 606
🔥Exp: 12839752/13979158
❤️Hp: 572/1449
🔋Stamina: 24/27 ⏰59min
💧Mana: 894/894
💰98 👝1389 💎4

🎽Equipment +197⚔️+166🛡
🎒Bag: 11/15 /inv


Pet:
🐎 stud +4⚡️ Sif (14 lvl) 😁 /pet

State:
🛌Rest /myshop_open

More: /hero"""


hero_pattern = compile(r'[\d\D]+!\n+'
                       r'(?P<castle_emoji>[\d\D])(?P<guild_emoji>[^\w]+)?'
                       r'(\[(?P<guild_tag>\w{2,3})\])?(?P<name>[\w _]{4,16}) '
                       r'(?P<primary_class>\w+)'
                       r' of (?P<castle>\w+) Castle\n+'
                       r'.+Level: (?P<level>\d+)[\D]+(?P<lvl_percent>[0-9]+.+[0-9]+).+\n+'
                       r'.+Atk: (?P<atk>\d+)[\D]+Def: (?P<def>\d+)\n+'
                       r'.+Exp: (?P<exp>\d+)[\D]\d+\n+'
                       r'.+Hp: (?P<hp>\d+)/\d+\n+'
                       r'.+Stamina: (?P<stamina>\d+)/(?P<max_stamina>\d+)(.+)?\n+'
                       r'(.+Mana: (?P<mana>\d+)/\d+\n+)?'
                       r'\D+(?P<gold>\d+)(\D+(?P<pogs>\d+)(\D+(?P<diamonds>\d+))?)?\n+'
                       r'\W+Equipment ((\+(?P<eq_atk>\d+)⚔)?(\D+(?P<eq_def>\d+))?)?.+\n+'
                       r'.+\n+'
                       r'(Pet:\n(?P<pet_emoji>[^\w ])[\w ]+?(?P<pet>\w+) (?P<pet_enchant>\+\d[^ ]+) (?P<pet_name>[\w ]+) \((?P<pet_level>\d+)'
                       r' lvl\) (?P<pet_status>[^ ]+) /pet\n+)?'
                       r'State:\n(?P<state>.+)\n+'
                       r'[\d\D]+')
                       
mobs = """You met some hostile creatures. Be careful:
Forbidden Blacksmith lvl.70
  ╰ golem minion, bow vulnerability
Forbidden Blacksmith lvl.70

/fight_5qwt8UFBvoDfzMrVFnZz"""
 
if __name__ == '__main__':
    import re

    # match = re.match(hero_pattern, test_text)
    # print(match)
    # print(test_text[match.start():match.end()] == test_text)
    # print(match.groupdict())
    
    pattern = r'lvl.\d{2}'
    lvl_list = re.findall(pattern, mobs)
    lvl = [int(x[4:]) for x in lvl_list]
    print(lvl)
    