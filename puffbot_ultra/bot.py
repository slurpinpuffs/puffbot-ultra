from server_list import ServerList
from youtube_community_tab import CommunityTab

import asyncio

import json
import os
import requests

import discord
from discord.ext import commands

EXPIRATION_TIME = 1 * 60 * 60

CURRENT_DIRECTORY = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(CURRENT_DIRECTORY, "config.json")

f = open(CONFIG_PATH)
config = f.read()
token = json.loads(config)["token"]
prefix = json.loads(config)["prefix"]

description = "A bot that gets YouTube community post updates."

activity = discord.CustomActivity(name="Keeping people updated!", emoji=discord.PartialEmoji.from_str("🩷"))

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix=prefix, description=description, intents=intents, activity=activity)

servers = ServerList()


@bot.event
async def on_ready():
    """Confirm bot login to Discord API and continually check for updates."""
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

    while True:
        await check_all_for_updates()
        await asyncio.sleep(60)


@bot.event
async def on_guild_join(guild):
    """When joining Discord server, add server to server list."""
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


@bot.command(description="Remove a YouTube channel to track posts on.")
async def removeytchannel(ctx, channel_name: str):
    try:
        # Gets server id of where command was called
        server_id = ctx.message.guild.id
        server = servers.get_server_by_id(server_id)

        if server == -1:
            raise Exception
        else:
            if channel_name in server.yt_channels:

                server.remove_yt_channel(channel_name)
                servers.save()
                await ctx.send(f'Successfully added {channel_name} to YT channel list.')
            else:
                await ctx.send(f'Failed! {channel_name} is not currently being tracked on this server.')
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


async def check_all_for_updates():
    """Check all servers in server list for new posts."""
    print("Checking for updates in all servers...")
    for server in servers.servers:
        await check_for_updates(server.server_id)


async def check_for_updates(server_id):
    """Check a server for new YouTube channel posts. If new post found, post_update() is called."""
    server = servers.get_server_by_id(server_id)
    for channel in server.yt_channels:
        ct = CommunityTab(channel)
        ct.load_posts(expire_after=EXPIRATION_TIME)
        post = ct.posts[0]  # Loads most recent post

        # Checks if post_id matches recent post_id.
        if post.post_id != server.yt_channels[channel]:
            await post_update(server_id, post, channel)


async def post_update(server_id, community_post, yt_channel):
    """Push a YouTube community post to a Discord server."""
    server = servers.get_server_by_id(server_id)

    post_thumbnails = community_post.get_thumbnails()
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
            image_count = download_thumbnails(post_thumbnails, yt_channel)
            file_list = []
            filename_template = f'channels/{yt_channel}/img'
            for x in range(image_count):
                file_list.append(discord.File(f'{filename_template}{x}.jpg'))
            await update_channel.send(f'[Post from {yt_channel}]:\n{post_text}', files=file_list)
            print(f"\n[Post {community_post.post_id} with {image_count} images]")
            print(f"\t{community_post.get_text()}")
    else:
        pass


def download_thumbnails(thumbnails, yt_channel):
    """Download images in channel-specific directory, return number of images."""
    channel_dir = "channels/" + yt_channel

    if not os.path.exists(channel_dir):
        os.mkdir(channel_dir)

    image_index = 0
    image_count = 0
    for image_set in thumbnails:
        try:
            url = image_set[-1]["url"]

            data = requests.get(url).content
            f = open(f"{channel_dir}/img{image_index}.jpg", "wb")
            f.write(data)
            f.close()
            image_count += 1
        except Exception:
            print("Failed to download image.")
        image_index += 1
    return image_count


# Runs the bot with Discord API token from config.json.
bot.run(token)
