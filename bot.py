import discord
import time
import asyncio
import hashlib
import random
from discord.ext import commands

client = commands.Bot(command_prefix="!")
token = YOUR-TOKEN
GUILD = YOUR-SERVER-ID
joined = 0
messages = 0


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild == GUILD:
            break

        print(f"""Ah yes, {client.user} is now connected to Discord on Guild {guild.name}, {guild.id}!""")


@client.event
async def on_member_join(member):
    global joined
    joined += 1
    for channel in member.guild.channels:
        if str(channel).find("general") != -1:
            await channel.send(f"""Welcome to the server, {member.mention}!""")


@client.event
async def on_member_remove(member):
    for channel in member.guild.channels:
        if str(channel).find("general") != -1:
            await channel.send(f"""Well, if you ask me, {member.name} deserved to be removed.""")


@client.event
async def on_guild_channel_create(channel):
    await channel.send(f"""Welcome to the new channel, {channel.name}!""")


@client.event
async def on_guild_channel_delete(channel):
    id = client.get_guild(GUILD)

    for c in id.channels:
        if str(c).find("general") != -1:
            await c.send(f"""Channel {channel.name} was deleted.""")
            break


@client.event
async def on_guild_channel_update(before, after):
    await after.send(f"""{before.name} now is called {after.name}""")


@client.event
async def on_guild_join(guild):
    for channel in guild.channels:
        if channel.name == "general":
            await channel.send("Hi, thanks for welcoming me to your server. Check !help for a list of commands")
            break

@client.command(name = "kick", help = "Kicks a user")
async def kick(ctx, user : discord.Member, reason = None):
    await user.kick(reason = reason)

@client.event
async def on_guild_role_create(role):
    id = client.get_guild(GUILD)
    for channel in id.channels:
        if channel.name == "general":
            await channel.send("New role created.")
            break


@client.command(name = "create-channel", help = "creates a new channel with the given name")
async def createChannel(ctx, channelName):

    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channelName)
    if not existing_channel:
        print(f"""Creating a new channel: {channelName}""")
        await guild.create_text_channel(channelName)

@client.command(name = "rps", help = "Rock Paper Scissors")
async def rps(ctx, choice):
    choices = ["rock", "paper", "scissor"]

    res = random.choice(choices)
    await ctx.send(res)

@client.command(name = "hello", help = "Says hello")
async def sayHello(ctx):
    await ctx.send("Hello there!")


@client.command(name = "birthday", help = "Says Happy Birthday to a User")
async def sayHB(ctx, name):
    await ctx.send("Happy Birthday, " + str(name).capitalize() + "!")

@client.command(name = "echo", help = "echoes back the message sent")
async def echo(ctx, *args):
    message = ""
    for word in args:
        message += word + " "

    await ctx.send(message)

@client.command(name = "encrypt", help = "encryptes a message")
async def md5(ctx, *args):
    message = ""
    for word in args:
        message += word + " "

    encryptedRes = hashlib.md5(message.encode())
    await ctx.send(encryptedRes.hexdigest())


@client.command(name = "callouts", help = "gives a link to image of CSGO Callouts")
async def giveURL(ctx, map):

    if map.lower() == "mirage":
        await ctx.send("Mirage: https://steamuserimages-a.akamaihd.net/ugc/771726758015167515/920A3B2823E12A734E4BBED38FC518FE6626D9BE/")
    elif map.lower() == "inferno":
        await ctx.send("Inferno: https://steamuserimages-a.akamaihd.net/ugc/763846954789928908/456494D0616C3DD65431B8E5E4C843E92FF08114/")
    elif map.lower() == "cache":
        await ctx.send("Cache: https://steamuserimages-a.akamaihd.net/ugc/788604629983432599/D6B07179997628242DF87282F063B4B0454839A1/")
    elif map.lower() == "dust":
        await ctx.send("Dust 2: https://steamuserimages-a.akamaihd.net/ugc/849347535114322925/AE8CE3B6FF828B3EF09779408A13788ED3BC99A6/?imw=512&imh=513&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true")
    elif map.lower() == "list":
        await ctx.send("Current Maps: Mirage, Inferno, Cache, Dust")


async def update_stats():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as file:
                file.write(f"Time: {int(time.time())}, Messages: {messages}, Members Joined: {joined}\n")

                messages = 0
                joined = 0

                await asyncio.sleep(100)

        except Exception as ex:
            print(ex)
            asyncio.sleep(100)


client.loop.create_task(update_stats())
client.run(token)
