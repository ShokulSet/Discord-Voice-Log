import json

config = {"guild_id": "channel_id"}
exclude = {"guild_id": "list_of_channel_id"}

with open("bot_config.json","wt") as w:
        temp = json.dumps(config, indent=4)
        w.write(temp)