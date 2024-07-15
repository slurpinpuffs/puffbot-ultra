from server import Server
from youtube_community_tab import Post

test_server = Server("nothing")
test_server.add_yt_channel("Kenadian")
test_server.check_for_updates()