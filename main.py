import discord
from discord.ext import commands
import json
from enum import Enum

token = 'Nzc0NjgwMzExMTk1ODkzODAw.X6bTQw.yjYLZGEBc6PVOWS5PiyXdaNsKVg'
client = commands.Bot(command_prefix = '$')

directions = ['⬆','⬇','⬅','➡']

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def echo(ctx, *, message):
    await ctx.send(message)
    print(message)

@client.command()
async def whoami(ctx):
    name = str(ctx.author).split('#')
    await ctx.send(name[0])

@client.command()
async def startgame(ctx):
    data = json.load('saves.txt') #Loads the JSON file and saves it as a var called data
    #TODO: Write a statement that checks if a user already has save data and ask to confirm if they want to erase previous save
    #TODO: Make sure when a user is confirming to delete the save that it is the same user and no one else can confirm a delete save

    data['users'].append({
        'name': f'{ctx.author}'
    })

    #Writes to the JSON file
    with open('saves.txt', 'w') as outfile:
        json.dump(data, outfile)

@client.command()
async def action(ctx):
    message = await ctx.send("What direction would you like to go?")

    #Puts all the direction emojis under the message
    for direction in directions:
        await message.add_reaction(direction)

    def check(reaction, user):
        return str(reaction.emoji) in directions and user == ctx.author
    reaction, user = await client.wait_for('reaction_add', check = check)
    await ctx.send(reaction)

@client.command()
async def react(ctx):
    message = await ctx.send('I want to kill myself')
    await message.add_reaction('👍')



client.run(token)#Runs the bot