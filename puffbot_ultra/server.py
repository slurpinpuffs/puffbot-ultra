from youtube_community_tab import CommunityTab
import requests
import os
from PIL import Image
import json

EXPIRATION_TIME = 1 * 60 * 60


class Server:
    def __init__(self, server_id, yt_channels=None, update_channel_id=None):
        self.server_id = server_id
        if yt_channels is None:
            self.yt_channels = {}  # Instantiate empty dict
        else:
            self.yt_channels = yt_channels  # Dict with channel names matched to last updates
        self.update_channel_id = update_channel_id  # Which channel to post in

    def get_id(self):
        return self.server_id
    
    def get_yt_channels(self):
        return self.yt_channels
    
    def set_update_channel_id(self, discord_channel_id):
        self.update_channel_id = discord_channel_id
    
    def add_yt_channel(self, channel_name):
        # Adds new yt channel to channel list and initializes latest community post
        self.yt_channels[channel_name] = ""

    def remove_yt_channel(self, channel_name):
        self.yt_channels.pop(channel_name)

    def set_recent_post(self, channel_name, recent_post_id):
        # Saves new recent post to dict
        self.yt_channels[channel_name] = recent_post_id

    def download_thumbnails(self, thumbnails, yt_channel):
        # Downloads images in channel-specific directory, returns number of images
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
