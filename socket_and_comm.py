import socket


class SocketClientServer:
    def __init__(self, server_address, server_port):
        self.host = server_address
        self.port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_client(self):
        try:
            self.socket.connect((self.host, self.port))
            print("[INFO]: La connection au serveur a Réussie ")
        except ConnectionRefusedError:
            print("[ERROR]: Echec de connection au serveur")
        # connecter(self.socket, self.host, self.port)

    def start_server(self):
        self.socket.bind((self.host, self.port))


def build_network(moi, sites, hosts, init_port):
    network = []
    for site in sites:
        if site != moi:
            port = init_port + site
            socketclient = SocketClientServer(hosts[site], port)
            socketclient.start_client()
            canal = socketclient.socket
            network.append(canal)

    return network
