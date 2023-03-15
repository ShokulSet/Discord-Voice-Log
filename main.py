import discord
import json
from dotenv import load_dotenv
import os
import atexit

load_dotenv()
bot_token = os.getenv('bot_token')

#Open the config file
with open("bot_config.json","rt") as r:
    config = json.load(r)
with open("exclusion.json","rt") as r:
    exclude = json.load(r)

TIPS =   '''Hello this is Discord bot made by Shokul#3557
To set the log channel up, simply type :
> !log #CHANNEL_NAME
If you have any suggestion feel free to contact me.'''

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

#Recive the configuration message
@bot.event
async def on_message(message):

    if message.author == bot.user:
        return
    
    if (message.content[0:4]) == "!log":
        if message.content[6] != "#" or len(message.content) != 27:
            await message.reply('This is not a valid channel, please try again.', mention_author=False)
            return
        log_channel = message.content[7:-1]
        config.update({message.guild.id: log_channel}) 
        temp = json.dumps(config, indent=4)
        with open("bot_config.json","wt") as w:
            w.write(temp)
        await message.reply(f'Ok, I will start the VC log at <#{log_channel}>', mention_author=False)
        channel = bot.get_channel(int(log_channel))
        await channel.send('For now on, I will send VC log here')

    if (message.content[0:8]) == "!exclude":
        if message.content[10] != "#" or len(message.content) != 31:
            await message.reply('This is not a valid channel, please try again.', mention_author=False)
            return
        exclude_channel = message.content[11:-1]
        exclude.update({message.guild.id: exclude_channel})
        temp = json.dumps(exclude, indent=4)
        with open("exclusion.json","wt") as w:
            w.write(temp)
        await message.reply(f'Ok, I will no longer send log from <#{exclude_channel}>', mention_author=False)

    if message.content.startswith("!chelp"):
        await message.reply(TIPS, mention_author=False)

@bot.event
async def on_voice_state_update(member, before, after):

    # print(f"Member : {member.name} \n Before : {before} \n After : {after} \n")
    # with open("exclusion.json","rt") as r:
    #     exclude = json.load(r)

    with open("bot_config.json","rt") as r:
        config = json.load(r)
    channel_id = config[str(member.guild.id)]
    channel = bot.get_channel(int(channel_id))

    if (before.channel == None and after.channel != None):
        # print(f"{member.name} joined {after.channel.name}")
        await channel.send(f"{member.name} joined {after.channel.name}")
    elif (before.channel != None and after.channel == None):
        # print(f"{member.name} left {before.channel.name}")
        await channel.send(f"{member.name} left {before.channel.name}")
    else:
        print(f"{member.name} did something else")

def exit_handler():
    print(config)
    print(exclude)
    
    with open("bot_config.json","wt") as w:
        temp = json.dumps(config, indent=4)
        w.write(temp)

    with open("exclusion.json","wt") as w:
        temp = json.dumps(exclude, indent=4)
        w.write(temp)
    print('Bot is closing successfully')

atexit.register(exit_handler)
bot.run(bot_token)