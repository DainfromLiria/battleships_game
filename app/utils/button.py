"""
    Class represented one button.
"""
from typing import Tuple
import pygame as pg
# utils
from utils.settings import COLORS
from utils.helper import draw_rect, draw_text


class Button:
    """Class represented one button.

        Attributes:
            rect - pg.Rect - rectangle that represented the button.
            text - str - name of the button.
            font_size - int - font size of the button's name.
            color - Tuple[int, int, int] - button color. Now button can only be gray.
    """
    def __init__(self, dest: Tuple[int, int], size: Tuple[int, int],
                 text: str, font_size: int) -> None:
        """Create one button.

        Attributes:
            dest - Tuple[int, int] - destination of the button.
            size - Tuple[int, int] - width and height of the button.
            text - str - name of the button.
            font_size - int - font size of the button's name.
        """
        self.rect = pg.Rect(dest[0], dest[1], size[0], size[1])
        self.text = text
        self.font_size = font_size
        self.color = COLORS["GRAY"]

    def is_pressed(self, x: int, y: int) -> bool:
        """Check if button was pressed.

        Attributes:
            x - int - x position of user input.
            y - int - y position of user input.
        Return:
            bool - True if button was pressed, False otherwise.
        """
        return self.rect.collidepoint(x, y)

    def draw(self, offset: int = 3):
        """Draw button with text

        Attributes:
            offset - int - offset from left side of the rectangle. By default, is 3.
        """
        draw_rect(self.rect, self.color, 0)
        dest = (self.rect.x + (self.rect.size[0] // offset), self.rect.y)
        draw_text(self.text, dest, self.font_size)
