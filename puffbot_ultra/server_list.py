from puffbot_ultra.server import Server
import json

SAVE_PATH = "./servers_save.txt"


class ServerList:
    def __init__(self):
        self.servers = []  # List of saved Server objects
        self.load()

    def get_servers(self):
        return self.servers

    def get_server_by_id(self, server_id):
        for server in self.servers:
            if server.get_id() == server_id:
                return server
        return -1
    
    def add_server(self, new_server):
        for server in self.servers:
            if server == new_server:
                pass
        self.servers.append(new_server)

    def load(self):
        try:
            f = open(SAVE_PATH, "r")
            save_json = f.read()
            saved_list = json.loads(save_json)
            for saved_server in saved_list:
                self.servers.append(Server(**saved_server))
            print("Successfully loaded in saved server list.")
        except Exception:
            print("Failed to load saved server list.")

    def save(self):
        with open(SAVE_PATH, "w") as file:
            json.dump([server.__dict__ for server in self.servers], file)

    def check_all_updates(self):
        for server in self.servers:
            server.check_for_updates()
