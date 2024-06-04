"""
    Class represented one cell on the board.
"""
from typing import Tuple
# utils
from utils.settings import GRID_PARAMS, COLORS
from utils.helper import get_rect, draw_rect, draw_cross, draw_circle


class Cell:
    """Class represented one cell on the board.

    Attributes:
        x - int - x coordinate
        y - int - y coordinate
        state - int - state of the cell:
            0 - empty cell
            1 - part of the ship (not hit)
            2 - hit part of the ship
            3 - miss
            4 - dead ship
            -1 - mouse on the cell
    """
    def __init__(self, x: int, y: int, state: int):
        """Initialize new cell by input x,y coordinates and set init state."""
        self.x = x
        self.y = y
        self.state = state

    def get_state(self) -> int:
        """Return current state of the cell."""
        return self.state

    def get_coords(self) -> Tuple[int, int]:
        """Return x and y coordinate of the cell."""
        return self.x, self.y

    def set_state(self, new_state: int) -> None:
        """Set new state for cell.

        Attributes:
            new_state - int (from -1 to 4) - new state of the cell
        """
        self.state = new_state

    def draw_cell(self, offset: int) -> None:
        """Draw one cell. Color sets by state of cell.

        Attributes:
            offset - int - can be FG_OFFSET or SG_OFFSET (left or right table)
        """
        c_size = GRID_PARAMS["CELL_SIZE"]
        rect = get_rect(offset, (self.x, self.y), (c_size, c_size))
        if self.state in (1, 0):
            draw_rect(rect, COLORS["BLUE_0"], 1)
        elif self.state == 2:
            draw_rect(rect, COLORS["BLUE_0"], 1)
            draw_cross(rect, COLORS["YELLOW"], 2)
        elif self.state == -1:
            draw_rect(rect, COLORS["GREEN"], 3)
        elif self.state == 3:
            draw_rect(rect, COLORS["GRAY"], 1)
            draw_circle(rect, COLORS["BLACK"], 3)
        elif self.state == 4:
            draw_rect(rect, COLORS["RED"], 2)
            draw_cross(rect, COLORS["RED"], 2)
