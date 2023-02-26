import discord
import json

#Open the config file
with open("bot_config.json","rt") as r:
    config = json.load(r)
    
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

bot_token = config["bot_token"]

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

#Recive the configuration message
@bot.event
async def on_message(message):
    # print(message.content)
    if message.author == bot.user:
        return
    
    if (message.content[0:4]) == "!log":
        if message.content[6] != "#":
            await message.channel.send('This is not a valid channel please try again.')
            return 
        log_channel = message.content[7:-1]
        config[message.guild.id] = log_channel
        temp = json.dumps(config, indent=4)
        with open("bot_config.json","wt") as w:
            w.write(temp)
        await message.channel.send(f'Ok I will start the VC log at <#{log_channel}>')
        channel = bot.get_channel(int(log_channel))
        await channel.send('For now on, I will send VC log here')

    if message.content.startswith("!chelp"):
        await message.channel.send('Hello this is Discord bot made by Shokul#3557 \nTo set the log channel up, simply type : \n > !log #CHANNEL_NAME \n\n If you have any suggestion feel free to contact me.')

@bot.event
async def on_voice_state_update(member, before, after):
    # print(f"Member : {member.name} \n Before : {before} \n After : {after} \n")
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

bot.run(bot_token)