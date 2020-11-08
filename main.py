import discord
from discord.ext import commands
import json
import datetime
import os
import random
from enum import Enum

token = 'Nzc0NjgwMzExMTk1ODkzODAw.X6bTQw.yjYLZGEBc6PVOWS5PiyXdaNsKVg'

save_folder = os.path.abspath(os.getcwd())+"/saves"
client = commands.Bot(command_prefix = '$')

directions = ['⬆', '⬇', '⬅', '➡']
combat = ['🗡️', '🏃']

command_list = ['move']

async def combatEncounter(ctx):
    message = await ctx.send("You encounter an asshole. Do you fight or flee? Look I'm paid to code not write")
    for emoji in combat:
        await message.add_reaction(emoji)
    def check(reaction, user):
        return str(reaction.emoji) in combat and user == ctx.author
    reaction, user = await client.wait_for('reaction_add', check = check)

    if(reaction.emoji == '🗡️'):
        await ctx.send('⚔️So you have chosen to fight⚔️')
        with open(f'{save_folder}/{ctx.author}.json') as f:
            data = json.load(f)
        def check(reaction, user):
            return str(reaction.emoji) in data['weapons'].values() and user == ctx.author
        message = await ctx.send('Please choose what weapon to use')
        for weapon in data['weapons'].values():
            await message.add_reaction(weapon)
        reaction, user = await client.wait_for('add_reaction', check = check)
        print('got here')
        await ctx.send(f'You attacked with your {data["weapons"].keys()[data["weapons"].values().index(reaction)]}')
        #TODO: Implement combat system where health changes

    elif (reaction.emoji == '🏃'):
        await ctx.send('So you have chosen to flee')
    else:
        await ctx.send('The bot is broken! SEND HELP!!')

loot = {
    'Sword': '🗡️',
    'Shield': '🛡️'
}

async def lootEncounter(ctx):
    RNJesus = random.randrange(2)
    with open(f'{save_folder}/{ctx.author}.json') as f:
        data = json.load(f)
    message = await ctx.send(f'You found a {list(loot)[RNJesus]}!')
    await message.add_reaction(loot[list(loot)[RNJesus]])
    data[list(loot)[RNJesus]] = loot[list(loot)[RNJesus]]

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
async def play(ctx):
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

        json_read = "file_err"

        #TODO: Needs a way to read the savefile after it has created. The JSON file is there, but it is not formatted back to objects
        with open(save_path_guess) as f:
            json_read = json.load(f)

        if flag:
            message_load = 'Welcome, '+json_read['name']+". Please enter the journey."
        else:
            message_load = 'Welcome back, '+json_read['name']+". Commands?"

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
            'infection': False,
            'symptoms': {},
            'tested': {},
            'items': {},
            'equipment': {},
            'weapons': {'Fist': '✊'}
        }

        with open(save_path_guess, 'w') as f:
            json.dump(json_file, f)

    def command_select(m):
        return (m.content in command_list) and m.channel == ctx.channel and m.author == ctx.author

    json_read = await loadsave(ctx.author)

    reaction = await client.wait_for('message', check=command_select)
    await ctx.send('You have selected: '+str(reaction.content))

@client.command()
async def action(ctx):
    message = await ctx.send("What direction would you like to go?")

    #Puts all the direction emojis under the message
    for direction in directions:
        await message.add_reaction(direction)

    def check(reaction, user):
        return str(reaction.emoji) in directions and user == ctx.author
    reaction, user = await client.wait_for('reaction_add', check = check)
    #TODO: Make the movement matter (right now it doesnt matter what direction you pick)

    RNJesus = random.randrange(20)
    if RNJesus == 19:
        await ctx.send('🍆Your dick is huge🍆')
    else:
        #Look I know that this is terrible code but Python is stupid and doesnt have switch statements, and I couldn't be bothered to make lamdas or enum functions so deal with it; I have other shit to do and you guys are not helping
        RNJesus = random.randrange(2)
        if RNJesus == 0:
            await combatEncounter(ctx)
        elif RNJesus == 1:
            await lootEncounter(ctx)


@client.command()
async def react(ctx):
    message = await ctx.send('I want to kill myself')
    await message.add_reaction('👍')

client.run(token) #Runs the bot