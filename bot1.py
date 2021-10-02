import discord
from discord.utils import get
from discord.ext import commands

tokenfilepath = "C:\\Users\\Max\\Downloads\\tokens.txt"

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_message(message):

  messageContent = message.content

  if messageContent == '!start6292':
      await message.delete()
      await message.channel.send('Welcome to Max’s Cord Bot!')

  elif messageContent == "!token":
      with open(tokenfilepath, "r") as f:
        tokenlist = f.readlines()
        await message.channel.send('loading '+ str(len(tokenlist))+' tokens')
        for token in tokenlist:
          await message.channel.send(token)
        await message.channel.send('What would you like to do with these tokens?')
        await message.channel.send('____________________________________________')
        await message.channel.send('DM someone, Join a server')

  elif messageContent == "DM someone":
    await message.channel.send('Please input User Info')
    await message.channel.send('For example: DMUSER - xxxxx#1111 ')

  elif messageContent.startswith("DM USER - "):
    await client.send_message(messageContent.replace("DMUSER", ""), "Nice to meet you!")

client.run('ODcyMTQwNjM3ODE2ODg5NDI0.YQliQw.en1iWUsiUN4JITJvcstIemISgwA')