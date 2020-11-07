import discord

token = 'Nzc0NjgwMzExMTk1ODkzODAw.X6bTQw.yjYLZGEBc6PVOWS5PiyXdaNsKVg'
client = discord.Client() #Creates the bots client


@client.event
async def on_message(message):
    #So the bot doesnt reply to itself
    if message.author == client.user:
        return

    if(message.content == '!hello'):
        await message.channel.send('Hello World')

client.run(token)#Runs the bot