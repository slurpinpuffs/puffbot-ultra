class Server:
    def __init__(self, server_id, yt_channels=None, update_channel_id=None):
        """Initialize server object with Discord server ID."""
        self.server_id = server_id
        if yt_channels is None:
            self.yt_channels = {}  # Instantiate empty dict
        else:
            self.yt_channels = yt_channels  # Dict with channel names matched to last updates
        self.update_channel_id = update_channel_id  # Which channel to post in
    
    def set_update_channel_id(self, discord_channel_id):
        """Set Discord channel where updates will be sent."""
        self.update_channel_id = discord_channel_id
    
    def add_yt_channel(self, channel_name):
        """Add new YT channel to yt_channels dict and initializes the latest community post."""
        self.yt_channels[channel_name] = ""

    def remove_yt_channel(self, channel_name):
        """Remove given channel from yt_channels dict."""
        self.yt_channels.pop(channel_name)

    def set_recent_post(self, channel_name, recent_post_id):
        """Save new recent post to yt_channels dict."""
        self.yt_channels[channel_name] = recent_post_id
