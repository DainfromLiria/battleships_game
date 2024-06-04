"""
    Class for server side. Server is for max 2 players.
"""

import socket
import pickle
import copy
from typing import Tuple
from _thread import start_new_thread
from utils.settings import NETWORK
from game.game import Game


class Server:
    """Class for server side. Server is for max 2 players.

    Attributes:
        s - socket - server socket.
        game - List[Game, Game] - game for first and second player.
        current_player - int - last input player number. First player = 0.
        chat_msg - List[str] - list of all sent messages in chat.
    """
    def __init__(self):
        """Create one server."""
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4 with TCP
        # bind server IPv4 address to port
        try:
            self.s.bind(("0.0.0.0", NETWORK["PORT"]))
        except socket.error as e:
            print(e)
        self.s.listen()
        print("Server up...")
        self.game = [Game(), Game()]
        self.curr_player = 0
        self.chat_msg = []

    def begin_conn(self, conn: socket.socket, player: int) -> bool:
        """Check count of connected players.

        Attributes:
            conn - socket - socket.
            player - int - player number.
        Return:
            bool - True if count of connected players is greater than 2.
        """
        if player > 1:
            conn.send(pickle.dumps("max_player_count"))
            print(f"[ERROR] Max player count for the server is 2, now: {player + 1}")
            self.curr_player -= 1
            conn.close()
            return False
        conn.send(pickle.dumps(player))
        return True

    def get_move(self, conn: socket.socket, player: int, enemy: int, data: Tuple):
        """Send Game object to player by player number.
        If input is 'move', in additional update enemy (player1) for player
        and update fleet and board for enemy.
        At the end, set is_my_move for enemy on True.

        Attributes:
            conn - socket - socket.
            player - int - player number.
            enemy - int - enemy number.
            data - Tuple[Any] - data from player.
        """
        if data[0] == "move":
            self.game[player].enemy = copy.deepcopy(data[1])
            self.game[player].is_my_move = data[2]
            self.game[enemy].player.fleet = data[1].fleet
            self.game[enemy].player.board = data[1].board
            self.game[enemy].player.invert_player()
            if self.game[player].is_my_move is False:
                self.game[enemy].is_my_move = True
        conn.sendall(pickle.dumps(self.game[player]))

    def set_ships(self, conn: socket.socket, player: int, enemy: int, data: Tuple):
        """Set player's board and fleet (player0) and set enemy's board and fleet (player1).
        Invert fleet for redraw ships on another board (board player1).
        At the end, check if both players are ready and if are
        set is_my_move on True for the last ready player. Send Game object to player
        by his global id on server.

        Attributes:
            conn - socket - socket.
            player - int - player number.
            enemy - int - enemy number.
            data - Tuple[Any] - data from player.
        """
        self.game[player].player.board = copy.deepcopy(data[1])
        self.game[player].player.fleet = copy.deepcopy(data[2])
        self.game[enemy].enemy.board = data[1]
        self.game[enemy].enemy.fleet = data[2]
        self.game[enemy].enemy.invert_player()
        self.game[player].player_ready = True
        self.game[enemy].enemy_ready = True
        if self.game[player].player_ready and self.game[player].enemy_ready:
            self.game[player].is_my_move = True
        conn.sendall(pickle.dumps((self.game[player])))

    def reset_game(self, conn: socket.socket, player: int, enemy: int) -> None:
        """Reset game for the player. For enemy set has_enemy on 1,
        so enemy connected (reset set it on 0) and save enemy username.

        Attributes:
            conn - socket - socket.
            player - int - player number.
            enemy - int - enemy number.
        """
        self.game[player].reset()
        self.game[player].has_enemy = 1
        self.game[enemy].has_enemy = 1
        self.game[player].enemy.username = self.game[enemy].player.username
        # if other enemy already press restart button and set his ships.
        if self.game[enemy].player_ready and not self.game[enemy].enemy_ready:
            self.game[player].enemy_ready = True
        conn.sendall(pickle.dumps(self.game[player]))

    def set_get_username(self, conn: socket.socket, player: int, enemy: int, data: Tuple):
        """Send username of the enemy to player. If set_user_name, in additional
        save username of the player and set it to enemy game as username of enemy.

        Attributes:
            conn - socket - socket.
            player - int - player number.
            enemy - int - enemy number.
            data - Tuple[Any] - data from player.
        """
        if data[0] == "set_user_name":
            self.game[player].player.username = data[1]
            self.game[enemy].enemy.username = data[1]
        conn.sendall(pickle.dumps((self.game[enemy].player.username,
                                   self.game[player].has_enemy)))

    def client_thread(self, conn, player: int):
        """Thread for one client.

        Attributes:
            conn - socket - socket.
            player - int - player number.
        """
        if not self.begin_conn(conn, player):
            return
        enemy = 0 if player == 1 else 1
        if player == 1:
            self.game[player].has_enemy = 1
            self.game[enemy].has_enemy = 1
        while True:
            try:
                data = pickle.loads(conn.recv(NETWORK["MSG_SIZE"]))
                if not data:
                    print("Disconnected")
                    break

                if data[0] == "chat":
                    if len(data[1]) > len(self.chat_msg):
                        self.chat_msg = data[1]
                    conn.sendall(pickle.dumps(self.chat_msg))
                elif data[0] in ("set_user_name", "get_enemy_name"):
                    self.set_get_username(conn, player, enemy, data)
                elif data[0] == "set_user_ships":
                    self.set_ships(conn, player, enemy, data)
                elif data[0] in ("move", "get"):
                    self.get_move(conn, player, enemy, data)
                elif data[0] == "reset":
                    self.reset_game(conn, player, enemy)
            except EOFError as e:
                print(e)
                break

        print("Lost connection")
        self.game[player].reset()
        if self.game[enemy].has_enemy != 0:
            self.game[enemy].has_enemy = 2
        self.chat_msg = []
        self.curr_player = 0
        conn.close()

    def server_thread(self):
        """Server thread"""
        while True:
            conn, _ = self.s.accept()
            start_new_thread(self.client_thread, (conn, self.curr_player))
            self.curr_player += 1

    def run(self) -> None:
        """Main method that runs the server."""
        start_new_thread(self.server_thread, ())
        while True:
            try:
                pass
            except KeyboardInterrupt:
                print("Server down...")
                self.s.close()


if __name__ == "__main__":
    server = Server()
    server.run()
