from server import Server
from server_list import ServerList
from youtube_community_tab import Post
from youtube_community_tab import CommunityTab

import requests
import os

import json

import discord
from discord.ext import commands
import random

EXPIRATION_TIME = 1 * 60 * 60

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


@bot.command(description="Force bot to post new updates for a server's channels.")
async def update(ctx):
    await check_for_updates(ctx.message.guild.id)


async def check_for_updates(server_id):
    server = servers.get_server_by_id(server_id)
    for channel in server.yt_channels:
        ct = CommunityTab(channel)
        ct.load_posts(expire_after=EXPIRATION_TIME)
        post = ct.posts[0]  # Loads most recent post

        # Checks if post_id matches recent post_id.
        if post.post_id != server.yt_channels[channel]:
            await post_update(server_id, post, channel)


async def post_update(server_id, community_post, yt_channel):
    server = servers.get_server_by_id(server_id)

    # TODO: Post to selected Discord channel in server, save as recent post in dict
    post_thumbnails = community_post.get_thumbnails()  # TODO: Check if there are thumbnails (in json).
    # If there are, post with thumbnails
    post_text = community_post.get_text()
    server.set_recent_post(yt_channel, community_post.post_id)
    servers.save()

    # If post doesn't have thumbnails, post text
    if server.update_channel_id is not None:  # Check if server has update channel set
        update_channel = bot.get_channel(server.update_channel_id)
        if not post_thumbnails:
            await update_channel.send(f'[Post {community_post.post_id}]\n{post_text}')
            print(f"\n[Post {community_post.post_id}]")
            print(f"\t{post_text}")
        else:  # If post has thumbnails, download and post thumbnails
            image_count = server.download_thumbnails(post_thumbnails, yt_channel)
            # TODO: Reduce redundant code when making post to Discord WITH images
            file_list = []
            filename_template = f'channels/{yt_channel}/img'
            for x in range(image_count):
                file_list.append(discord.File(f'{filename_template}{x}.jpg'))
            await update_channel.send(f'[Post from {yt_channel}]:\n{post_text}', files=file_list)
            print(f"\n[Post {community_post.post_id} with {image_count} images]")
            print(f"\t{community_post.get_text()}")
    else:
        pass


bot.run(token)
