# Puffbot ULTRA
Discord bot that pulls YouTube community posts from given YouTube channels and posts them to a Discord channel. Works across multiple Discord servers.

If you'd like to run your own instance of this bot:
- Set your Discord Bot API token in config.json.
- Install requirements from requirements.txt.
- Run bot.py.
- You can also set a custom command prefix in the config (default is "pu!").

To get the bot running on your Discord server:
- Invite it to your server <b>while the script is running</b>.
  - You can use the <a href="https://discord.com/oauth2/authorize?client_id=1270867215062667334">link here</a> to invite it to your server, or use your own link if running your own instance.
- Use "pu!setupdatechannel <Discord channel ID>" to set which text channel you want the bot to post updates in.
- Use "pu!addytchannel <YouTube channel name>" to add a new YouTube channel to track community posts for. You can keep the @ sign in the channel name or not.
  
The bot will check for updates across all servers its joined every 60 seconds.
