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

Battle of the seven castles in 2h 28 minutes!

🦅Minion GA Sentinel of Highnest Castle
🏅Level: 61
⚔️Atk: 299 🛡Def: 810
🔥Exp: 2056654/2283221
❤️Hp: 1375/1375
🔋Stamina: 7/25 ⏰15min
💧Mana: 610/610
💰10805 👝1362 💎156

🎽Equipment +111⚔️+252🛡
🎒Bag: 6/15 /inv


Pet:
🐷 guardian pig Coronel (27 lvl) 😁 /pet

State:
🛡Defending 🦅Highnest Castle

More: /hero"""

hero_pattern = compile(r'[\d\D]+!\n+'
                       r'(?P<castle_emoji>[\d\D])(?P<guild_emoji>[^\w]+)?'
                       r'(\[(?P<guild_tag>\w{2,3})\])?(?P<name>[\w _]+) '
                       r'(?P<primary_class>\w+)'
                       r' of (?P<castle>\w+) Castle\n+'
                       r'.+Level: (?P<level>\d+)\n+'
                       r'.+Atk: (?P<atk>\d+).+Def: (?P<def>\d+)\n+'
                       r'.+Exp: (?P<exp>\d+)/\d+\n+'
                       r'.+Hp: (?P<hp>\d+)/\d+\n+'
                       r'.+Stamina: (?P<stamina>\d+)/(?P<max_stamina>\d+)(.+)?\n+'
                       r'(.+Mana: (?P<mana>\d+)/\d+\n+)?'
                       r'\D+(?P<gold>\d+)(\D+(?P<pogs>\d+)(\D+(?P<diamonds>\d+))?)?\n+'
                       r'\W+Equipment ((\+(?P<eq_atk>\d+)⚔)?(\D+(?P<eq_def>\d+))?)?.+\n+'
                       r'.+\n+'
                       r'(Pet:\n(?P<pet_emoji>[^\w ]) \w+ (?P<pet>\w+) (?P<pet_name>[\w ]+) \((?P<pet_level>\d+)'
                       r' lvl\) (?P<pet_status>[^ ]+) /pet\n+)?'
                       r'State:\n(?P<state>.+)\n+'
                       r'[\d\D]+')

if __name__ == '__main__':
    import re
    match = re.match(hero_pattern, test_text)
    print(test_text[match.start():match.end()] == test_text)
    print(match.groupdict())
