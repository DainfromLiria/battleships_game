"""
    Network part for player.
"""
import socket
import pickle
from typing import Any
from utils.settings import NETWORK


class Network:
    """Network part for player.

    Attributes:
        client - socket - socket.
        addr - Tuple[int, int] - IPv4 of server and server's port.
        connected - Any - data that returned server after connection.
    """
    def __init__(self):
        """Set up client network part for player and connect to server."""
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (NETWORK['SERVER'], NETWORK['PORT'])
        self.connected = self.connect()

    def connect(self) -> Any:
        """First connection to server. Connect to server and get first data from server.

        Return:
            Any - server answer (global user id on server).
            bool - False if server has already maximum count of connections
            or server part raise error.
        """
        try:
            self.client.connect(self.addr)
        except (ConnectionRefusedError, ConnectionResetError):
            print('Connection lost')
            return False
        server_out = pickle.loads(self.client.recv(NETWORK["MSG_SIZE"]))
        if server_out == "max_player_count":
            return False
        return server_out

    def send(self, data: Any) -> Any:
        """Send data from player to server and get and return server answer.

        Attributes:
            data - Any - data that player sends to server.
        Return:
            Any - server answer.
        """
        self.client.send(pickle.dumps(data))
        return pickle.loads(self.client.recv(NETWORK["MSG_SIZE"]))
