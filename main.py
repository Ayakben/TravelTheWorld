import discord
from discord.ext import commands
import json
import datetime
import os

token = 'Nzc0NjgwMzExMTk1ODkzODAw.X6bTQw.yjYLZGEBc6PVOWS5PiyXdaNsKVg'

save_folder = os.path.abspath(os.getcwd())+"/saves"
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
async def action(ctx):
    # Separate Logic that just retrieves jsonfile read based on the tag (str)
    # If there is no file, create one
    # Deletion of save is handled with different command
    def loadsave(tag):

        if not os.path.isdir(save_folder):
            os.mkdir(save_folder)

        save_path_guess = save_folder + "/" + tag + ".json"

        if not os.path.isdir(save_path_guess):
            newsave(tag)

        json_read = "file_err"

        #TODO: Needs a way to read the savefile after it has created. The JSON file is there, but it is not formatted back to objects
        with open(save_path_guess) as f:
            json_read = json.load(f)

        print(json_read)

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
    def newsave(tag):
        save_path_guess = save_folder + "/" + tag + ".json"
        json_file = {
            'name': tag,
            'file_creation': datetime.datetime.now(),
            'last_action': "",
            'current_loc': "",
            'fund': 0,
            'infection': False,
            'symptoms': {},
            'tested': {},
            'items': {},
            'equipment': {}
        }

        with open(save_path_guess, 'w') as f:
            json.dumps(json_file, f)

    loadsave(ctx.author)


client.run(token)#Runs the bot