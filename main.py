import discord
from discord.ext import commands
import json

token = 'Nzc0NjgwMzExMTk1ODkzODAw.X6bTQw.yjYLZGEBc6PVOWS5PiyXdaNsKVg'
client = commands.Bot(command_prefix = '$')

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


client.run(token)#Runs the bot