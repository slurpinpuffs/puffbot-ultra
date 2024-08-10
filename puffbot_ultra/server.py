class Server:
    def __init__(self, server_id, yt_channels=None, update_channel_id=None):
        self.server_id = server_id
        if yt_channels is None:
            self.yt_channels = {}  # Instantiate empty dict
        else:
            self.yt_channels = yt_channels  # Dict with channel names matched to last updates
        self.update_channel_id = update_channel_id  # Which channel to post in
    
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
