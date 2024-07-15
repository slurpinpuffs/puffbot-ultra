from youtube_community_tab import CommunityTab
import requests
from PIL import Image
import json

EXPIRATION_TIME = 1 * 60 * 60

class Server:
    #TODO: Decide which class should watch for commands in servers
    
    def __init__(self, server_id):
        self.server_id = server_id
        self.yt_channels = {} # Dict with channel names matched to last updates
        self.posting_discord_channel = "" # Which channel to post in

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
    
    @staticmethod
    def post_to_discord(community_post):
        # TODO: Post to selected Discord channel in server, save as recent post in dict
        post_thumbnails = community_post.get_thumbnails() # TODO: Check if there are thumbnails (in json). If there are, post with thumbnails
        post_text = community_post.get_text()

        # If post doesn't have thumbnails, post text
        if not post_thumbnails:
            print(f"\n[Post {community_post.post_id}]")
            print(f"\t{community_post.get_text()}")
        # If post has thumbnails, download and post thumbnails 
        else:
            image_count = Server.download_thumbnails(post_thumbnails)
            # TODO: Reduce redundant code when making post to Discord WITH images
            print(f"\n[Post {community_post.post_id} with {image_count} images]")
            print(f"\t{community_post.get_text()}")
            

    def set_recent_post(self, channel_name, recent_post_id):
        # Saves new recent post to dict
        self.yt_channels[channel_name] = recent_post_id

    @staticmethod
    def download_thumbnails(thumbnails):
        image_index = 0
        image_count = 0
        for image_set in thumbnails:
            try:
                url = image_set[-1]["url"]

                data = requests.get(url).content
                f = open(f"img{image_index}.jpg", "wb")
                f.write(data)
                f.close()
                image_count += 1
            except:
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
                Server.post_to_discord(post)
                self.set_recent_post(channel, post.post_id)

        pass # TODO: Iterate through saved YT channels to check for new community posts. Post if new