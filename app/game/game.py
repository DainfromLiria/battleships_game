"""
    Class that represented whole game for one player.
"""
import sys
import pygame as pg
# utils
from utils.settings import GRID_PARAMS, COLORS, BASE, FONT_SIZE
from utils.helper import get_mouse_pos, is_in_range, draw_coords, draw_text
from utils.button import Button
# src objects
from chat.chat import Chat
from player.player import Player
from online.network import Network
from menus.end_menu import EndMenu


class Game:
    """Class that represented whole game for player.

    Attributes:
        chat - Chat - chat object that create chat for current player.
        player - Player - represented player.
        enemy - Player - represented enemy.
        end_menu - EndMenu - menu that user can see after win or defeat
        has_enemy - int:
            0 - wait enemy.
            1 - enemy connected.
            2 - enemy leave.
        enemy_ready - bool - True if enemy is ready for play.
        player_ready - bool - True if player is ready for play.
        is_my_move - bool - True if players time to move, False otherwise.
        ready_button - Button - represented ready button in set phase.
        randomise_button - Button - represented randomise button in set phase.
    """
    def __init__(self):
        """Creates game object."""
        self.chat = Chat()
        self.player = Player(0)
        self.enemy = Player(1)
        self.end_menu = EndMenu()
        self.has_enemy = 0
        self.enemy_ready = False
        self.player_ready = False
        self.is_my_move = False
        self.ready_button = Button((BASE["WIDTH"] - 1060, BASE["HEIGHT"] - 200),
                                   (120, 35), "Ready",
                                   FONT_SIZE["SET_PHASE"])
        self.randomise_button = Button((BASE["WIDTH"] - 1220, BASE["HEIGHT"] - 200),
                                       (120, 35), "Randomise",
                                       FONT_SIZE["SET_PHASE"])

    def update(self, game: 'Game') -> None:
        """Update current game object by input game object.
        Used for maintaining same game state as on the server.

        Attributes:
            game - Game - input game object.
        """
        self.player = game.player
        self.enemy = game.enemy
        self.is_my_move = game.is_my_move
        self.has_enemy = game.has_enemy
        self.enemy_ready = game.enemy_ready
        self.player_ready = game.player_ready

    def reset(self) -> None:
        """Full game reset for new game."""
        self.has_enemy = 0
        self.enemy_ready = False
        self.player_ready = False
        self.is_my_move = False
        self.player.reset()
        self.enemy.reset()

    def draw_green_rect(self) -> None:
        """Draw green rect on possible cell for users move."""
        row, col = get_mouse_pos(self.enemy.offset)
        if is_in_range(row, col):
            state = self.enemy.get_cell_state(row, col)
            if state in (0, 1):
                self.enemy.set_cell_state(row, col, -1)
                self.enemy.draw()
                self.enemy.set_cell_state(row, col, state)

    def all_draw(self, net: Network) -> None:
        """Draw all game objects.

        Attributes:
            net - Network - used to draw updated chat.
        """
        screen = pg.display.get_surface()
        screen.fill(COLORS["WHITE"])
        draw_coords(self.player.username, self.enemy.username)
        self.player.draw()
        self.enemy.draw()
        self.draw_green_rect()
        if not self.player_ready:
            self.ready_button.draw()
            self.randomise_button.draw(6)
        if self.has_enemy == 0 or (self.player_ready and not self.enemy_ready):
            dest = (BASE["WIDTH"] // 2 + 105, BASE["HEIGHT"] // 2 - 80)
            draw_text("Waiting for enemy...", dest, 40)
        if not self.is_my_move and (self.player_ready and self.enemy_ready):
            dest = (BASE["WIDTH"] // 2 + 105, BASE["HEIGHT"] // 2 - 80)
            draw_text("Enemy's move...", dest, 40)
        self.chat.draw(net)
        pg.display.flip()

    def in_chat(self, net: Network) -> None:
        """If user enters into the chat.
        Player is in this method until chat is active.

        Attributes:
            net - Network - players online part.
        """
        while True:
            if not self.chat.chat_loop():
                break
            self.update(net.send(("get",)))
            self.all_draw(net)

    def set_ships(self, net: Network) -> None:
        """Set ships on player's board. Send it to the server,
        receive enemy ships positions and set it on local enemy board.
        Firstly player also send his user and receive enemy username.

        Attributes:
            net - Network - player part of online.
        """
        self.enemy.username, self.has_enemy = net.send(("set_user_name", self.player.username))
        self.player.reset()

        current_ship = None
        old_orient = None
        self.chat = Chat()  # reset chat
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pg.mouse.get_pos()
                    if self.randomise_button.is_pressed(x, y):
                        self.player.reset()
                    elif self.ready_button.is_pressed(x, y):
                        self.update(net.send(("set_user_ships",
                                              self.player.board, self.player.fleet)))
                        return
                    elif self.chat.is_in_chat(x, y):
                        self.in_chat(net)
                    else:
                        current_ship = self.player.fleet.set_dragging()
                        old_orient = current_ship.orientation if current_ship is not None \
                            else None
                elif (event.type == pg.MOUSEBUTTONUP and current_ship is not None
                      and event.button == 1):
                    row, col = get_mouse_pos()
                    current_ship.update_position(row, col, self.player.board, old_orient)
                    current_ship.dragging = False
                    current_ship = None
                elif event.type == pg.MOUSEMOTION and current_ship is not None:
                    current_ship.rect.topleft = event.pos
                elif event.type == pg.MOUSEWHEEL and current_ship is not None:
                    orient = 0 if current_ship.orientation == 1 else 1
                    y, x = get_mouse_pos()
                    current_ship.set_orientation(orient, x, y)
            if self.has_enemy == 0:
                self.enemy.username, self.has_enemy = net.send(("get_enemy_name",
                                                                self.player.username))
            self.all_draw(net)

    def move(self, net: Network) -> None:
        """Method that manage players move.

        Attributes:
            net - Network - player part of online.
        """
        row, col = get_mouse_pos(GRID_PARAMS["SG_OFFSET"])
        if is_in_range(row, col) and self.is_my_move:
            c_state = self.enemy.get_cell_state(row, col)
            if c_state == 1:
                self.enemy.set_cell_state(row, col, 2)  # Hit
            elif c_state == 0:
                self.enemy.set_cell_state(row, col, 3)  # Miss
                self.is_my_move = False
            self.player.fleet.update_sunk(self.player.board)
            self.enemy.fleet.update_sunk(self.enemy.board)
            self.update(net.send(("move", self.enemy, self.is_my_move)))

    def game_loop(self, usr_name) -> int:
        """Main game loop. Connection to the server, setting ships, moves.

        Attributes:
            usr_name - str - username of player.
        Return:
            int - 0 if user wants to return to the main menu.
                  1 if connection error (automatically return to main menu).
                  2 if enemy left after game (automatically return to main menu).
        """
        # connect to the server and set ships.
        net = Network()
        if net.connected is False:
            return 1
        self.player.username = usr_name
        self.set_ships(net)

        while True:
            if self.has_enemy == 2:
                return 2
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    x, y = pg.mouse.get_pos()
                    # chat
                    if self.chat.is_in_chat(x, y):
                        self.in_chat(net)
                    # players move
                    elif self.player_ready and self.enemy_ready:
                        self.move(net)
            # check on sunk
            if self.enemy.fleet.is_sunk_fleet() or self.player.fleet.is_sunk_fleet():
                if not self.end_menu.run(self.enemy.fleet.is_sunk_fleet()):
                    return 0
                self.update(net.send(("reset",)))
                self.set_ships(net)
            else:
                self.all_draw(net)
                self.update(net.send(("get",)))
