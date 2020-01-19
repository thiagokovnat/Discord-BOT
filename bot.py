import discord
import time
import asyncio
import hashlib
import random
from discord.ext import commands



client = commands.Bot(command_prefix="!")
token = YOUR-TOKEN
GUILD = YOUUR-SERVER-ID
joined = 0
messages = 0


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild == GUILD:
            break

        print(f"""{client.user} is now connected to Discord on Guild {guild.name}, {guild.id}!""")


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


@client.command(name = "callouts", help = "shows an image of CSGO Callouts")
async def giveURL(ctx, map):

    Embedded = discord.Embed()
    if map.lower() == "mirage":
        Embedded.set_image(url = "https://steamuserimages-a.akamaihd.net/ugc/771726758015167515/920A3B2823E12A734E4BBED38FC518FE6626D9BE/")
        Embedded.set_footer(text = "Mirage")
        await ctx.send(content = None, embed = Embedded)
    elif map.lower() == "inferno":
        Embedded.set_image(url = "https://steamuserimages-a.akamaihd.net/ugc/763846954789928908/456494D0616C3DD65431B8E5E4C843E92FF08114/")
        Embedded.set_footer(text = "Inferno")
        await ctx.send(content=None, embed = Embedded)
    elif map.lower() == "cache":
        Embedded.set_image(url = " https://steamuserimages-a.akamaihd.net/ugc/788604629983432599/D6B07179997628242DF87282F063B4B0454839A1/")
        Embedded.set_footer(text = "Cache")
        await ctx.send(content=None, embed = Embedded)
    elif map.lower() == "dust":
        Embedded.set_image(url="https://steamuserimages-a.akamaihd.net/ugc/849347535114322925/AE8CE3B6FF828B3EF09779408A13788ED3BC99A6/?imw=512&imh=513&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true")
        Embedded.set_footer(text="Dust 2")
        await ctx.send(content=None, embed = Embedded)
    elif map.lower() == "list":
        Embedded.add_field(name = "Mirage", value = "!callouts mirage", inline = False)
        Embedded.add_field(name = "Inferno", value = "!callouts inferno", inline = False)
        Embedded.add_field(name = "Cache", value = "!callouts cache", inline = False)
        Embedded.add_field(name = "Dust 2", value = "!callouts dust", inline = False)
        await ctx.send(content = None, embed = Embedded)

#@client.command(name = "stats", help = "gives your current CSGO Stats")
#async def getStats(ctx, steamId):
    #url = "https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key=12A1D1DE83F9932934EDD6DF2BA00463&steamid=" + str(steamId)
    #r = requests.get(url).json()

    #stats = {
       # 'total_kills': r['playerstats']['stats'][0]['value'],  # total kills
      #  'total_deaths': r['playerstats']['stats'][1]['value'],  # total deaths
     #   'total_time': r['playerstats']['stats'][2]['value']  # total time played
    #}

   # await ctx.send(f"""Total Kills: {stats["total_kills"]}, Total Deaths: {stats['total_deaths']}, Time Played: {stats['total_time']/3600}h. KD: {stats["total_kills"]/stats['total_deaths']}""")

@client.command(name = "ping", help = "returns current bot ping")
async def ping(ctx):

    await ctx.send("Current bot ping: " + str(client.latency) + "ms")

@client.command(name = "ban", help = "Bans player from server")
async def ban(ctx, User : discord.Member, reason = None):
    await User.ban(reason = reason)

@client.command(name = "clear", help = "deletes x messages")
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount = 10):
    await ctx.channel.purge(limit = amount)

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
