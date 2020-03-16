import os
import discord
import asyncio
import pdb
import schedule
import randomword
import json

guild = os.getenv('DISCORD_GUILD')
token = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == guild:
            print(guild)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == 'randomword!':
        response = randomword.getRandomWord("dictionary.db")
        payload = json.loads(response)
        embed = discord.Embed(title=payload.get('title'), url=payload.get('url'), description=payload.get('description'))
        await message.channel.send(embed=embed)
        
        #.send("[" + payload.get('title') + "](" + payload.get('url') + ")" + "\r\n" + payload.get('description'))

client.run(token)