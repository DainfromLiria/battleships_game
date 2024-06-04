"""
    All helper functions for this game.
"""
from typing import Tuple
import pygame as pg
from utils.settings import FONT_SIZE, FONT_NAME, COLORS, GRID_PARAMS, USERNAME_DEST


def draw_text(text: str, dest: Tuple[int, int], font_size: int = FONT_SIZE["MAIN"],
              font_name: str = FONT_NAME["GAME"],
              color: Tuple[int, int, int] = COLORS["BLACK"]) -> None:
    """Draw inputed text on the screen.

    Attributes:
        text - str - text to draw.
        dest - Tuple[int, int] - x,y position of the text.
        font_size - int - size of the text.
        font_name - str - name of the text font.
        color - Tuple[int, int, int] - RGB color of the text.
    """
    screen = pg.display.get_surface()
    font = pg.font.SysFont(font_name, font_size)
    font_text = font.render(text, True, color)
    screen.blit(font_text, dest)


def draw_coords(player: str, enemy: str) -> None:
    """Draw alphanumeric coordinates for enemy and player boards.
    Also draw player and enemy usernames.

    Attributes:
        player - str - player username.
        enemy - str - enemy username.
    """
    draw_text(player, USERNAME_DEST["LEFT"])
    draw_text(enemy, USERNAME_DEST["RIGHT"])
    for i, char in enumerate("ABCDEFGHIJ"):
        draw_text(str(i+1), (115 + (i+1) * GRID_PARAMS["CELL_SIZE"], 120))
        draw_text(str(i+1), (675 + (i+1) * GRID_PARAMS["CELL_SIZE"], 120))
        draw_text(char, (120, 150 + i * GRID_PARAMS["CELL_SIZE"]))
        draw_text(char, (680, 150 + i * GRID_PARAMS["CELL_SIZE"]))


def get_mouse_pos(offset: int = GRID_PARAMS["FG_OFFSET"]) -> Tuple[int, int]:
    """Get mouse position and convert it to position on the board.

    Attributes:
        offset - int - can be FG_OFFSET or SG_OFFSET (left or right table).
    Return:
        Tuple[int, int] - row and column on the board.
    """
    x, y = pg.mouse.get_pos()
    row = (y - GRID_PARAMS["FG_OFFSET"]) // GRID_PARAMS["CELL_SIZE"]
    col = (x - offset) // GRID_PARAMS["CELL_SIZE"]
    return row, col


def is_in_range(x: int, y: int) -> bool:
    """Check if input coordinates is in range [0, GRID_PARAMS["GRID_SIZE"]].

    Attributes:
        x - int - x coordinate.
        y - int - y coordinate.
    Return:
        bool - True if is in range, False otherwise.
    """
    grid_range = range(0, GRID_PARAMS["GRID_SIZE"])
    if x in grid_range and y in grid_range:
        return True
    return False


def draw_rect(rect: pg.Rect, color: Tuple[int, int, int], width: int) -> None:
    """Draw rect.

    Attributes:
        rect - pg.Rect - rectangle to draw.
        color - Tuple[int, int, int] - RGB color of the rect.
        width - int - width of the rect.
    """
    screen = pg.display.get_surface()
    pg.draw.rect(screen, color, rect, width)


def draw_cross(rect: pg.Rect, color: Tuple[int, int, int], width: int) -> None:
    """Draw cross inside the rect.

    Attributes:
        rect - pg.Rect - rectangle inside which will be drawn the cross.
        color - Tuple[int, int, int] - RGB color of circle.
        width - int - width of the cross.
    """
    screen = pg.display.get_surface()
    pg.draw.line(screen, color, rect.topleft, rect.bottomright, width)
    pg.draw.line(screen, color, rect.topright, rect.bottomleft, width)


def draw_circle(rect: pg.Rect, color: Tuple[int, int, int], radius: int) -> None:
    """Draw a circle inside the rect.

    Attributes:
        rect - pg.Rect - rectangle inside which will be drawn the circle.
        color - Tuple[int, int, int] - RGB color of circle.
        radius - int - circle radius.
    """
    screen = pg.display.get_surface()
    pg.draw.circle(screen, color, rect.center, radius)


def get_rect(offset: int, coords: Tuple[int, int], size: Tuple[int, int]) -> pg.Rect:
    """Create rectangle for ships and board cells.

    Attributes:
        offset - int - can be FG_OFFSET or SG_OFFSET (left or right table).
        coords - Tuple[int, int] - x and y coord of the rect.
        size - Tuple[int, int] - width and height of the rect.
    Return:
        pg.Rect - created rect.
    """
    fg_ofs = GRID_PARAMS["FG_OFFSET"]
    c_size = GRID_PARAMS["CELL_SIZE"]
    x, y = coords
    return pg.Rect(offset + x * c_size, fg_ofs + y * c_size, size[0], size[1])
