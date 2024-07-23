from server import Server
from server_list import ServerList
from youtube_community_tab import Post


if __name__ == "__main__":
    servers = ServerList()

    test_server = Server("nothing", {})
    test_server.add_yt_channel("MarisaHonkai")

    test_server_2 = Server("nonexistant", {})
    test_server_2.add_yt_channel("Kenadian")
    test_server_2.add_yt_channel("DiddySauce")
    
    servers.add_server(test_server)
    servers.add_server(test_server_2)
    servers.check_all_updates()
    servers.save()
    
    #servers.load()
    #servers.check_all_updates()