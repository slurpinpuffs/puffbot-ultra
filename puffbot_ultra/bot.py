from server import Server
from server_list import ServerList
from youtube_community_tab import Post

import json

import discord
from discord.ext import commands
import random

f = open("./config.json")
config = f.read()
token = json.loads(config)["token"]
print(token)

description = "A bot that gets YouTube community post updates."

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="p!", description=description, intents=intents)

servers = ServerList()


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.event
async def on_guild_join(guild):
    servers.add_server(guild.id)
    print(f'Successfully added {guild.name} to server list.')


@bot.command(description="Add new YouTube channel to track posts on.")
async def add_channel(ctx, channel_name: str):
    try:
        # Gets server id of where command was called
        server_id = ctx.message.guild.id
        server = servers.get_server_by_id(server_id)

        if server == -1:
            raise Exception
        else:
            server.add_yt_channel(channel_name)
    except Exception:
        await ctx.send("Failed! Please make sure a valid YouTube channel name was entered.")


bot.run(token)
