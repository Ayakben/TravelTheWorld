import discord
from discord.ext import commands
import json
import datetime
import os
import random
from enum import Enum

with open("token.json") as f:
    tokens = json.load(f)

token = ''
for piece in tokens['token']:
    token = token + piece
print(token)
save_folder = os.path.abspath(os.getcwd())+"/saves"
client = commands.Bot(command_prefix = '$')

directions = ['⬆', '⬇', '⬅', '➡']
combat = ['🗡️', '🏃']

command_list = ['move']

# Experimental weapon classes
class Weapon:
    def __init__(self, emote, damage, damage_reduction, chanceToHit):
        self.emote = emote
        self.damage = damage
        self.damage_reduction = damage_reduction
        self.chanceToHit = chanceToHit

weaponEnums = {
    'Fist': Weapon('✊' , 1, 0, .7),
    'Sword': Weapon('🗡️',3 ,0, .8),
    'Axe': Weapon('🪓', 5, 0, .6),
    'Shield': Weapon('🛡️', 0, 1, 1),
    'Super Shield': Weapon('🔰', 0, 2, 1)
}

class Monster:
    def __init__(self, health, damage_min, damage_max, chanceToHit):
        self.health = health
        self.damage_min = damage_min
        self.damage_max = damage_max
        self.chanceToHit = chanceToHit

monsterEnums = {
    'skeleton': Monster(5, 1, 1, .6),
    'zombie': Monster(3, 1, 1, .5)
}

#TODO: Implement either a state or flag system so that a player can only use certain commands while in the middle of an action

async def combatEncounter(ctx):
    with open(f'{save_folder}/{ctx.author}.json') as f:
        data = json.load(f)
    if data['state'] == 2:
        RNJesus = random.randrange(len(monsterEnums))
        monsterName = list(monsterEnums.keys())[RNJesus]
        message = await ctx.send(f"You encountered a(n) {monsterName}. Do you fight or flee?")
        for emoji in combat:
            await message.add_reaction(emoji)

        def check(reaction, user):
            return str(reaction.emoji) in combat and user == ctx.author


        reaction, user = await client.wait_for('reaction_add', check=check)

        if(reaction.emoji == '🗡️'):
            await ctx.send('⚔️You stand in front of the enemy. ⚔️')
            randomMonster = monsterEnums[monsterName] #This creates the instance of the monster the player will be fighting


            while True:
                message = await ctx.send('Choose your next weapon!')

                weaponEmotes = []
                for weapon in data['weapons']:
                    weaponEmotes.append(weaponEnums[weapon].emote)
                    await message.add_reaction(weaponEnums[weapon].emote)

                def checktwo(reaction, user):
                    return str(reaction.emoji) in weaponEmotes and user == ctx.author

                reaction, user = await client.wait_for('reaction_add', check=checktwo)

                #The player attacks
                for weapon in weaponEnums:
                    if(weaponEnums[weapon].emote == reaction.emoji):
                        await ctx.send(f'You choose the {weapon}.')
                        if(random.random() < weaponEnums[weapon].chanceToHit):
                            if weaponEnums[weapon].damage != 0:
                                await ctx.send(f'You hit the {monsterName} for {weaponEnums[weapon].damage} damage!')
                                randomMonster.health = randomMonster.health - weaponEnums[weapon].damage
                            else:
                                await ctx.send(f'You ready your {weapon}...')
                        else:
                            await ctx.send(f'You missed the enemy by moving the {weapon} too far!')
                        break
                if (randomMonster.health <= 0):
                    await ctx.send(f'The {monsterName} was killed.')
                    await ctx.send(f'Congrats on beating the {monsterName}!')
                    data['state'] = 2
                    break
                if (random.random() < randomMonster.chanceToHit):
                    damage = random.randint(randomMonster.damage_min, randomMonster.damage_max+1)
                    await ctx.send(f'The {monsterName} does {damage} damage to you.')
                    if weaponEnums[weapon].damage_reduction != 0:
                        await ctx.send(f'You used {weapon} to block the damage!')
                        preformat_damage = damage - weaponEnums[weapon].damage_reduction
                        if preformat_damage < 0:
                            preformat_damage = 0
                        await ctx.send(f'You blocked with {weapon} and reduced the damage to {preformat_damage}!')
                    await ctx.send(f'You have {data["health"]} left!')
                    data['health'] = data['health'] - preformat_damage
                    if data['health'] <= 0:
                        await ctx.send('Game over.')
                        data['state'] = 0
                        break
                else:
                    await ctx.send(f'The {monsterName} damage did not do anything.')
            with open(f'{save_folder}/{ctx.author}.json', 'w') as f:
                json.dump(data, f)
        elif (reaction.emoji == '🏃'):
            await ctx.send('So you have chosen to flee')
        else:
            await ctx.send('The bot is broken! SEND HELP!!')



async def lootEncounter(ctx):
    with open(f'{save_folder}/{ctx.author}.json') as f:
        data = json.load(f)
    RNJesus = random.randrange(1, len(weaponEnums))
    message = await ctx.send(f'You found a {list(weaponEnums.keys())[RNJesus]}!')
    await message.add_reaction(list(weaponEnums.values())[RNJesus].emote)
    if(list(weaponEnums.keys())[RNJesus] not in data['weapons']):
        data['weapons'].append(list(weaponEnums.keys())[RNJesus])
    else:
        await ctx.send(f'You already have a {list(weaponEnums.keys())[RNJesus]}.')
    data['state'] = 2
    with open(f'{save_folder}/{ctx.author}.json', 'w') as f:
        json.dump(data, f)

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def echo(ctx, *, message):
    await ctx.send(message)

@client.command()
async def whoami(ctx):
    name = str(ctx.author).split('#')
    await ctx.send(name[0])

@client.command()
async def inventory(ctx):
    data = None
    with open(f'{save_folder}/{ctx.author}.json') as f:
        data = json.load(f)
    message = await ctx.send(f'your inventory')
    weaponEmotes = []
    for weapon in data['weapons']:
        weaponEmotes.append(weaponEnums[weapon].emote)
        await message.add_reaction(weaponEnums[weapon].emote)

    with open(f'{save_folder}/{ctx.author}.json', 'w') as f:
        json.dump(data, f)


@client.command()
async def delete(ctx):
    def check(reaction, user):
        return str(reaction.emoji) in ['✔', '❌'] and user == ctx.author


    message = await ctx.send(f"Are you going to reset your save? (Y|N)")
    await message.add_reaction('✔')
    await message.add_reaction('❌')

    reaction, user = await client.wait_for('reaction_add', check=check)

    if reaction.emoji == '✔':
        save_path_guess = save_folder + "/" + str(user) + ".json"
        os.remove(save_path_guess)
        await ctx.send(f"Save deleted. Please use new game command to restart the game.")



@client.command()
async def newgame(ctx):
    message_load = ""

    # Separate Logic that just retrieves jsonfile read based on the tag (str)
    # If there is no file, create one
    # Deletion of save is handled with different command
    async def loadsave(tag):

        flag = False
        if not os.path.isdir(save_folder):
            os.mkdir(save_folder)

        save_path_guess = save_folder + "/" + str(tag) + ".json"

        if not os.path.isfile(save_path_guess):
            flag = True
            await newsave(tag)
        else:
            return None

        json_read = "file_err"

        #TODO: Needs a way to read the savefile after it has created. The JSON file is there, but it is not formatted back to objects
        with open(save_path_guess) as f:
            json_read = json.load(f)

        if flag:
            message_load = 'Welcome, '+json_read['name']+". Please enter the journey."
        else:
            message_load = 'Welcome back, '+json_read['name']+". "

        await ctx.send(message_load)

        return json_read

    # Creation of new file
    # Savefile contains in json file format
    # name
    # date and time of file creation
    # date and time of last action (used for
    # last action (string)
    # current location (string)
    # funds (number, this will be some sort of number that will be later calculated to current country's currency)
    # infection (number, days till recover. could be game over if this is true, but chance based)
    # symptoms (list)
    # tested (list)
    # items (list)
    # equipment (list)
    async def newsave(tag):
        save_path_guess = save_folder + "/" + str(tag) + ".json"
        json_file = {
            'name': str(tag),
            'file_creation': datetime.datetime.now().isoformat(),
            'last_action': "",
            'current_loc': "",
            'fund': 0,
            'health': 30,
            'state': 0,
            'infection': False,
            'symptoms': {},
            'tested': {},
            'items': {},
            'equipment': {},
            'weapons': ['Fist'] #'✊'
        }

        with open(save_path_guess, 'w') as f:
            json.dump(json_file, f)

    def command_select(m):
        return (m.content in command_list) and m.channel == ctx.channel and m.author == ctx.author

    json_read = await loadsave(ctx.author)

    if json_read is None:
        await ctx.send(f"You already have the save. Please enter move command!")
        return

    reaction = await client.wait_for('message', check=command_select)
    await ctx.send('You have selected: '+str(reaction.content))

@client.command()
async def move(ctx):
    message = await ctx.send("What direction would you like to go?")

    #Puts all the direction emojis under the message
    for direction in directions:
        await message.add_reaction(direction)

    def check(reaction, user):
        return str(reaction.emoji) in directions and user == ctx.author
    reaction, user = await client.wait_for('reaction_add', check = check)

    with open(f'{save_folder}/{ctx.author}.json') as f:
        data = json.load(f)
    data['state'] = 2
    with open(f'{save_folder}/{ctx.author}.json', 'w') as f:
        json.dump(data, f)

    #TODO: Make the movement matter (right now it doesnt matter what direction you pick)
    RNJesus = random.randrange(20)
    if RNJesus == 19:
        await ctx.send('You Win')
        with open(f'{save_folder}/{ctx.author}.json') as f:
            data = json.load(f)
        data['state'] = 0
        with open(f'{save_folder}/{ctx.author}.json', 'w') as f:
            json.dump(data, f)
    else:
        #Look I know that this is terrible code but Python is stupid and doesnt have switch statements, and I couldn't be bothered to make lamdas or enum functions so deal with it; I have other shit to do and you guys are not helping
        RNJesus = random.randrange(2)
        print("move")
        if RNJesus == 0:
            await combatEncounter(ctx)
        elif RNJesus == 1:
            await lootEncounter(ctx)



@client.command()
async def react(ctx):
    message = await ctx.send('I want to kill myself')
    await message.add_reaction('👍')

client.run(token) #Runs the bot