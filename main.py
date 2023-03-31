import discord
import json
from dotenv import load_dotenv
import os
import atexit
import time


def embed_join(member,after,before):
    embed=discord.Embed(title=member.name, description=f"📥 **{member.name}** joined **{after.channel.name}**", color=0x00db49)
    embed.set_thumbnail(url=member.display_avatar)
    embed.set_footer(text= time.ctime())
    return embed

def embed_leave(member,after,before):
    embed=discord.Embed(title=member.name, description=f"📤 **{member.name}** left **{before.channel.name}**", color=0xe00000)
    embed.set_thumbnail(url=member.display_avatar)
    embed.set_footer(text= time.ctime())
    return embed

def embed_move(member,after,before):
    embed=discord.Embed(title=member.name, description=f"🔁 **{member.name}** moved from **{before.channel.name}** to **{after.channel.name}**", color=0x00c8d6)
    embed.set_thumbnail(url=member.display_avatar)
    embed.set_footer(text= time.ctime())
    return embed

load_dotenv()
bot_token = os.getenv('bot_token')
TIPS =   '''Hello this is Discord bot made by Shokul#3557
To set the log channel up, simply type :
> !log #CHANNEL_NAME
If you have any suggestion feel free to contact me.'''

#Open the config file
with open("bot_config.json","rt") as r:
    config = json.load(r)

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
        await channel.send('Form now on, I will send VC log here')

    if message.content.startswith("!chelp"):
        await message.reply(TIPS, mention_author=False)

@bot.event
async def on_voice_state_update(member, before, after):

    # print(f"Member : {member.name} \n Before : {before} \n After : {after} \n")
    with open("bot_config.json","rt") as r:
        config = json.load(r)
    channel_id = config[str(member.guild.id)]
    channel = bot.get_channel(int(channel_id))

    if (before.channel == None and after.channel != None):
        print(f"{member.name} joined {after.channel.name}")
        # await channel.send(f"{member.name} joined {after.channel.name}")
        await channel.send(embed=embed_join(member,after,before))
    elif (before.channel != None and after.channel == None):
        print(f"{member.name} left {before.channel.name}")
        # await channel.send(f"{member.name} left {before.channel.name}")
        await channel.send(embed=embed_leave(member,after,before))
    elif (before.channel != None and after.channel != None and before.deaf == after.deaf and before.mute == after.mute and before.self_deaf == after.self_deaf and before.self_mute == after.self_mute and before.self_stream == after.self_stream and before.self_video == after.self_video and before.afk == after.afk):
        # await channel.send(f"{member.name} moved from {before.channel.name} to {after.channel.name}")
        await channel.send(embed=embed_move(member,after,before))
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