import discord
from discord.ext import commands
from discord.utils import get
import json
from discord.ext.commands import has_permissions, MissingPermissions
import asyncio

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("Ticket bot running...")

@bot.command()
async def help_me(ctx):
    em = discord.Embed(title="Auroris Tickets Help", description="", color=0x00a8ff)
    await ctx.send(embed=em)

#@bot.command()
async def new(ctx, message_content = ""):
    await bot.wait_until_ready()

    with open("data.json") as f:
        data = json.load(f)

    ticket_number = int(data["ticket-counter"])
    ticket_number += 1

    ticket_channel = await ctx.guild.create_text_channel("ticket-{}".format(ticket_number))
    await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)

    for role_id in data["valid-roles"]:
        role = ctx.guild.get_role(role_id)

        await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
    
    await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

    em = discord.Embed(title="New ticket from {}#{}".format(ctx.author.name, ctx.author.discriminator), description= "{}".format(message_content), color=0x00a8ff)

    await ticket_channel.send(embed=em)

    pinged_msg_content = ""
    non_mentionable_roles = []

    if data["pinged-roles"] != []:

        for role_id in data["pinged-roles"]:
            role = ctx.guild.get_role(role_id)

            pinged_msg_content += role.mention
            pinged_msg_content += " "

            if role.mentionable:
                pass
            else:
                await role.edit(mentionable=True)
                non_mentionable_roles.append(role)
        
        await ticket_channel.send(pinged_msg_content)

        for role in non_mentionable_roles:
            await role.edit(mentionable=False)
    
    data["ticket-channel-ids"].append(ticket_channel.id)

    data["ticket-counter"] = int(ticket_number)
    with open("data.json", 'w') as f:
        json.dump(data, f)
    
    created_em = discord.Embed(title="Auroris Tickets", description="Your ticket has been created at {}".format(ticket_channel.mention), color=0x00a8ff)
    
    await ctx.send(embed=created_em)

@bot.command()
async def close(ctx):
    with open('data.json') as f:
        data = json.load(f)

    if ctx.channel.id in data["ticket-channel-ids"]:

        channel_id = ctx.channel.id

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "close"

        try:

            em = discord.Embed(title="Interest Tickets", description="Are you sure you want to close this ticket? Reply with `close` if you are sure.", color=0x00a8ff)
        
            await ctx.send(embed=em)
            await bot.wait_for('message', check=check, timeout=60)
            await ctx.channel.delete()

            index = data["ticket-channel-ids"].index(channel_id)
            del data["ticket-channel-ids"][index]

            with open('data.json', 'w') as f:
                json.dump(data, f)
        
        except asyncio.TimeoutError:
            em = discord.Embed(title="Auroris Tickets", description="You have run out of time to close this ticket. Please run the command again.", color=0x00a8ff)
            await ctx.send(embed=em)

        
@bot.command()
async def interest(ctx):
    page = discord.Embed (
        title = 'Which sport are you interested in?',
        description = '''
        '⚽': soccer ball
        '⚾': baseball
        '🥎': softball
        '🏀': basketball
        '🏐': volleyball
        Please click sport emoji you are interested in.
        ''',
        colour = discord.Colour.orange()
    )

    message = await ctx.send(embed = page)
    await message.add_reaction('⚽') #soccer ball
    await message.add_reaction('⚾') #baseball
    await message.add_reaction('🥎') #softball
    await message.add_reaction('🏀') #basketball
    await message.add_reaction('🏐') #volleyball

    def check(reaction, user):
        return user == ctx.author

    reaction = None

    while True:
        if str(reaction) == '⚽':
            await new(ctx, message_content="Welcome to Soccer Ball Ticket! If you wanna close, please type !close")
        elif str(reaction) == '⚾':
            await new(ctx, message_content="Welcome to Baseball Ticket! If you wanna close, please type !close")
        elif str(reaction) == '🥎':
            await new(ctx, message_content="Welcome to Softball Ticket! If you wanna close, please type !close")
        elif str(reaction) == '🏀':
            await new(ctx, message_content="Welcome to Basketball Ticket! If you wanna close, please type !close")
        elif str(reaction) == '🏐':
            await new(ctx, message_content="Welcome to Volleyball Ticket! If you wanna close, please type !close")
        
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout = 30.0, check = check)
            await message.remove_reaction(reaction, user)
        except:
            break

    await message.clear_reactions()
bot.run('ODczMjQ2MjI2MDEzOTEzMTA5.YQ1n7A.PSRzth7b-scgFehCtJEs6yhGI_8')
#bot.run('ODcyNDEwOTc4MTkxNTczMDQy.YQpeCQ.FCeibb_4ee1NkZAo2irmLhH2fLI')