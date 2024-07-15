from server import Server

class ServerList:
    def __init__(self):
        self.servers = [] # List of saved Server objects
        # TODO: If save json exists, load that list automatically

    def get_servers(self):
        return self.servers
    
    def add_server(self, server_id):
        # TODO: Check if server with same id exists in list already
        new_server = Server(server_id)
        self.servers.append(new_server)

    def load(self):
        pass # TODO: Load existing server list from json file

    def save(self):
        pass # TODO: Save server list to json file

    def check_all_updates(self):
        for server in self.servers:
            server.check_for_updates()
