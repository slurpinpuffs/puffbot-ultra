from youtube_community_tab import CommunityTab
import requests
import os
from PIL import Image
import json

EXPIRATION_TIME = 1 * 60 * 60


class Server:
    def __init__(self, server_id, yt_channels=None, posting_discord_channel=None):
        self.server_id = server_id
        if yt_channels is None:
            self.yt_channels = {}  # Instantiate empty dict
        else:
            self.yt_channels = yt_channels  # Dict with channel names matched to last updates
        self.posting_discord_channel = posting_discord_channel  # Which channel to post in

    def get_id(self):
        return self.server_id
    
    def get_yt_channels(self):
        return self.yt_channels
    
    def set_discord_channel(self, discord_channel):
        self.posting_discord_channel = discord_channel
    
    def add_yt_channel(self, channel_name):
        # Adds new yt channel to channel list and initializes latest community post
        self.yt_channels[channel_name] = ""

    def remove_yt_channel(self, channel_name):
        self.yt_channels.pop(channel_name)
    
    def post_to_discord(self, community_post, yt_channel):
        # TODO: Post to selected Discord channel in server, save as recent post in dict
        post_thumbnails = community_post.get_thumbnails()  # TODO: Check if there are thumbnails (in json).
        # If there are, post with thumbnails
        post_text = community_post.get_text()

        # If post doesn't have thumbnails, post text
        if not post_thumbnails:
            print(f"\n[Post {community_post.post_id}]")
            print(f"\t{post_text}")
        # If post has thumbnails, download and post thumbnails 
        else:
            image_count = self.download_thumbnails(post_thumbnails, yt_channel)
            # TODO: Reduce redundant code when making post to Discord WITH images
            print(f"\n[Post {community_post.post_id} with {image_count} images]")
            print(f"\t{community_post.get_text()}")

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

    def check_for_updates(self):
        for channel in self.yt_channels:
            ct = CommunityTab(channel)
            ct.load_posts(expire_after=EXPIRATION_TIME)
            post = ct.posts[0] # Loads most recent post

            # If recent post isn't saved as recent post, post and save it
            if post.post_id != self.yt_channels[channel]:
                self.post_to_discord(post, channel)
                self.set_recent_post(channel, post.post_id)

        pass # TODO: Iterate through saved YT channels to check for new community posts. Post if new