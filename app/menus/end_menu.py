"""
    Menu that is shown after user's win or defeat.
"""
import sys
import pygame as pg
# utils
from utils.settings import BASE, COLORS, FONT_SIZE, FONT_NAME
from utils.helper import draw_text
from utils.button import Button


class EndMenu:
    """Menu that is shown after users win or defeat.

    Attributes:
        return_button - Button - pressed this button user returns to main menu.
        restart_button - Button - pressed this button user restart the game.
        quit_button - Button - pressed this button user quit the game.
    """
    def __init__(self):
        """Initialize one end menu object."""
        self.return_button = Button((BASE["WIDTH"] // 2 - 150, BASE["HEIGHT"] // 2 - 90),
                                    (400, 50), "Return to main menu", FONT_SIZE["USERNAME"])
        self.restart_button = Button((BASE["WIDTH"] // 2 - 100, BASE["HEIGHT"] // 2 - 30),
                                     (300, 50), "Restart", FONT_SIZE["USERNAME"])
        self.quit_button = Button((BASE["WIDTH"] // 2 - 50, BASE["HEIGHT"] // 2 + 30),
                                  (200, 50), "Quit", FONT_SIZE["USERNAME"])

    def draw(self, is_win: bool) -> None:
        """Draw menu on the screen.

        Attributes:
            is_win - bool - True if the user win, False if lost.
        """
        text = "You win!" if is_win else "You lose!"
        dest = (BASE["WIDTH"] // 2 - 50, BASE["HEIGHT"] // 2 - 190)
        color = COLORS["GREEN"] if is_win else COLORS["RED"]
        draw_text(text, dest, FONT_SIZE["WINNER"], FONT_NAME["GAME"], color=color)
        self.return_button.draw(offset=16)
        self.restart_button.draw()
        self.quit_button.draw()

    def run(self, is_win: bool) -> bool:
        """Main loop of this menu.

        Attributes:
            is_win - bool - True if the user win, False if lost.
        Return:
            bool - True if restart the game (pressed restart_button),
            False if return to main menu (pressed return_button).
        """
        screen = pg.display.get_surface()
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
                    elif self.return_button.is_pressed(x, y):
                        return False
                    elif self.restart_button.is_pressed(x, y):
                        return True
            screen.fill(COLORS["WHITE"])
            self.draw(is_win)
            pg.display.flip()
