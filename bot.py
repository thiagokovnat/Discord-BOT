import discord
import time
import asyncio


client = discord.Client()
token = "BOT-TOKEN"
GUILD = SERVER-GUILD
joined = 0
messages = 0

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    global messages
    insults = ["example", "example1", "example2"]
    messages += 1
    id = client.get_guild(GUILD)

    if message.content.find("!hello") != -1:
        await message.channel.send("Hi, I am GameBOT!")

    elif message.content == "!users":
        await message.channel.send(f"""# of members: {id.member_count}""")

    elif message.content == "!help":
        embedded = discord.Embed(title = "Help", description = "Commands")
        embedded.add_field(name = "!hello", value = "Says Hi")
        embedded.add_field(name = "!users", value = "Lists all users")
        embedded.add_field(name = "Happy Birthday", value = "Wish a Happy Birthday to a user")
        embedded.add_field(name = "!usernames", value = "Gives all usernames on the server")
        await message.channel.send(content = None, embed = embedded)

    elif message.content.lower() == "happy birthday" or message.content.lower() == "feliz cumpleaños":
        await message.channel.send("Happy birthday, discord user!")
    elif message.content == "!usernames":
        for guild in client.guilds:
            if guild == GUILD:
                break

            members = '\n'.join([member.name for member in guild.members])
            await message.channel.send(members)
    else:
        split_message = str(message.content).split()

        for word in split_message:

            if word in insults:
                await message.channel.purge(limit = 1)
                await message.channel.send("A bad word was said, message deleted.")
                break

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
