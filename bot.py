import discord
from discord.ext import commands
from discord.utils import get
import json

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Client running...")
    for server in client.guilds:
        for channel in server.channels:
            if channel.name == 'general':
                await channel.send('Which sport are you interested in?')
                await channel.send('Please type !interest')

@client.event
async def on_member_join(member):
    print("Member joined: ", member)
    # channel = get(member.serverx.channels, name="general")
    # await member.send("welcome") 
    for server in client.guilds:
        for channel in server.channels:
            if channel.name == 'general':
                await channel.send(f'Welcome @{member.name}!')
                await channel.send('Which sport are you interested in?')
                await channel.send('Please type !interest')

client.run('ODcyMTQwNjM3ODE2ODg5NDI0.YQliQw.en1iWUsiUN4JITJvcstIemISgwA')