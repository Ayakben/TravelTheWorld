import discord
from discord.ext import commands

token = 'Nzc0NjgwMzExMTk1ODkzODAw.X6bTQw.yjYLZGEBc6PVOWS5PiyXdaNsKVg'
client = commands.Bot(command_prefix = '$')

@client.command()
async def ping(ctx):
    await ctx.send('Pong!')

client.run(token)#Runs the bot