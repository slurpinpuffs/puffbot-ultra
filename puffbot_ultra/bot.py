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
    servers.save()


@bot.command(description="Add new YouTube channel to track posts on.")
async def addytchannel(ctx, channel_name: str):
    try:
        # Gets server id of where command was called
        server_id = ctx.message.guild.id
        server = servers.get_server_by_id(server_id)

        if server == -1:
            raise Exception
        else:
            server.add_yt_channel(channel_name)
            servers.save()
            await ctx.send(f'Successfully added {channel_name} to YT channel list.')
    except Exception:
        await ctx.send("Failed! Please make sure a valid YouTube channel name was entered.")


@bot.command(description="Set channel in server to post updates in. Use channel ID, NOT name.")
async def setupdatechannel(ctx, channel_id: int):
    try:
        # Gets server id of where command was called
        server_id = ctx.message.guild.id
        server = servers.get_server_by_id(server_id)

        if server == -1:
            raise Exception(ValueError)
        else:
            channel = ctx.message.guild.get_channel_or_thread(channel_id)
            if channel is None:
                raise Exception(NameError)
            else:
                server.set_update_channel_id(channel_id)
                servers.save()
                await ctx.send("Successfully set updates channel.")
    except NameError:
        await ctx.send("Failed! Make sure a valid channel id is used.")
    except ValueError:
        await ctx.send("Failed! Server error.")


bot.run(token)
