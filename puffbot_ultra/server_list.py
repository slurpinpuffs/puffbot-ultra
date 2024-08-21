from server import Server
import json

SAVE_PATH = "./servers_save.json"


class ServerList:
    def __init__(self):
        """Initialize list of the bot's Discord servers."""
        self.servers = []  # List of saved Server objects
        self.load()

    def get_server_by_id(self, server_id):
        """Return Discord server with given server ID."""
        for server in self.servers:
            if server.server_id == server_id:
                return server
        return -1
    
    def add_server(self, new_server_id):
        """Add new Discord server to server list."""
        for server in self.servers:
            if server == new_server_id:
                pass

        new_server = Server(new_server_id)
        self.servers.append(new_server)

    def remove_server(self, server_id):
        """Remove Discord server from server list."""
        self.servers.remove(server_id)

    def load(self):
        """Load server list from json file."""
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
        """Save server list to json file."""
        with open(SAVE_PATH, "w") as file:
            json.dump([server.__dict__ for server in self.servers], file)