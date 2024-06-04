"""
    Main users menu.
"""
import sys
import time
import pygame as pg
# utils
from utils.settings import BASE, COLORS, FONT_SIZE, FONT_NAME
from utils.helper import draw_rect, draw_text
from utils.button import Button
# src.game
from game.game import Game


class MainMenu:
    """
        Main user's menu.

    Attributes:
        username - str - username of player.
        game - Game - player's game.
        not_connect - bool - True if user cannot connect to server.
        player_leave - bool - True if after game enemy left.
        input_box - pg.Rect - input box for entering username.
        play_button - Button - button for start the game.
        quit_button - Button - button for quit the game.
    """
    def __init__(self):
        """Create one main menu object."""
        self.username = ""
        self.game = Game()
        self.not_connect = False
        self.player_leave = False
        self.input_box = pg.Rect(BASE["WIDTH"] // 2 - 50, BASE["HEIGHT"] // 2 - 100, 445, 40)
        self.play_button = Button((self.input_box.x - 50, self.input_box.y + 50),
                                  (200, 50), "Play", FONT_SIZE["USERNAME"])
        self.quit_button = Button((self.input_box.x - 50, self.input_box.y + 120),
                                  (200, 50), "Quit", FONT_SIZE["USERNAME"])

    def draw_username(self) -> None:
        """Draw box for entering username and text entered by the user."""
        draw_rect(self.input_box, COLORS["GRAY"], 2)
        dest = (self.input_box.x - 150, self.input_box.y + 8)
        draw_text("Username: ", dest, FONT_SIZE["USERNAME"], FONT_NAME["CHAT"], COLORS["BLACK"])
        dest = (self.input_box.x + 5, self.input_box.y + 8)
        draw_text(self.username, dest, FONT_SIZE["USERNAME"], FONT_NAME["CHAT"], COLORS["BLACK"])

    def draw(self) -> None:
        """Draw all main menu objects."""
        screen = pg.display.get_surface()
        screen.fill(COLORS["WHITE"])
        dest = (self.input_box.x - 100, self.input_box.y - 150)
        draw_text("Battleships", dest, FONT_SIZE["WINNER"], FONT_NAME["GAME"])
        self.draw_username()
        self.play_button.draw()
        self.quit_button.draw()
        # draw error message
        if self.not_connect:
            draw_text("Cannot connect to the server!",(dest[0] + 50, dest[1] + 100),
                      font_size=FONT_SIZE["SET_PHASE"], color=COLORS["RED"])
        elif self.player_leave:
            draw_text("Player left!", (dest[0] + 50, dest[1] + 100),
                      font_size=FONT_SIZE["SET_PHASE"], color=COLORS["RED"])
        pg.display.flip()
        # wait 2 sec until user read text of the error.
        if self.not_connect:
            time.sleep(2)
            self.not_connect = False
        elif self.player_leave:
            time.sleep(2)
            self.player_leave = False

    def run(self) -> None:
        """Main menu loop. Run until user pressed quit button or close the program."""
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    x, y = pg.mouse.get_pos()
                    if self.quit_button.is_pressed(x, y):
                        pg.quit()
                        sys.exit()
                    elif self.play_button.is_pressed(x, y):
                        status = self.game.game_loop(self.username)
                        if status == 1:
                            self.not_connect = True
                        elif status in (2, 0):
                            self.player_leave = True
                            self.game.reset()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        self.username = self.username[:-1]
                    else:
                        # enter is not valid symbol
                        if len(self.username) < BASE["USERNAME_LEN"] and event.unicode != '\r':
                            self.username += event.unicode
            self.draw()
