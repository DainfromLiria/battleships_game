"""
    Class represented one ship on the board.
"""
import copy
from typing import Tuple
import pygame as pg

# src.map
from map.grid import Grid
from map.cell import Cell
# utils
from utils.settings import GRID_PARAMS, COLORS
from utils.helper import is_in_range, get_rect, draw_rect


class Ship:
    """Class represented one ship on the board.

    Attributes:
        size - int (form 1 to 4) - size of the ship.
        pos - list of Cell - position of the ship on the table.
        sunk - boolean - True if ship is sunk, False otherwise.
        orientation - int - 0 if horizontal, 1 if vertical.
        rect - Rect - pygame Rect for drawing the ship.
        dragging - bool - True if ship is dragging, False otherwise.
        offset - int - can be FG_OFFSET or SG_OFFSET (left or right table).
    """
    def __init__(self, size: int, offset: int):
        """Initialize one ship object"""
        self.size = size
        self.pos = []
        self.sunk = False
        self.orientation = 0
        self.rect = None
        self.dragging = False
        self.offset = offset

    def set_rect(self, x: int = None, y: int = None) -> None:
        """Set or update ship rect.
         Use input position of the first cell in pos list (first part of the ship)

        Attributes:
            x - int - x coordinate (if None => current first element pos)
            y - int - y coordinate (if None => current first element pos)
        """
        c_size = GRID_PARAMS["CELL_SIZE"]
        if x is None or y is None:
            x, y = self.pos[0].get_coords()
        if self.orientation == 0:
            self.rect = get_rect(self.offset, (x, y), (c_size, c_size * self.size))
        else:
            self.rect = get_rect(self.offset, (x, y), (c_size * self.size, c_size))

    def update_offset(self, offset: int) -> None:
        """Set new offset and redrew rect.

        Attributes:
            offset - int - can be FG_OFFSET or SG_OFFSET (left or right table).
        """
        self.offset = offset
        self.set_rect(self.offset)

    def add_pos(self, pos: Cell) -> None:
        """Add position of ship on board.

        Attributes:
            pos - Cell - cell that is part of the ship.
        """
        self.pos.append(pos)

    def is_ship_part(self, cell: Tuple[int, int]) -> bool:
        """Check if cell is a part of the ship.

        Attributes:
            cell - Tuple[int, int] - coordinates of the cell.

        Return:
            bool - True if cell is in pos list of this ship, False otherwise.
        """
        if len(self.pos) == 0:
            return False
        if cell in [self.pos[i].get_coords() for i in range(0, self.size)]:
            return True
        return False

    def set_sunk(self, grid: Grid) -> None:
        """Check if all cells in ship pos list have status 2 (hit)
           and if had, set status 4 (dead) for all these cells.

           Attributes:
               grid - Grid - grid with this ship.
        """
        if all(self.pos[i].state == 2 for i in range(0, self.size)):
            self.sunk = True
            for pos in self.pos:
                pos.set_state(4)
                grid.around_sunk_ship(pos)

    def set_orientation(self, orientation: int, x: int = None, y: int = None) -> None:
        """Update or set ship orientation and recreate ship's rect.

        Attributes:
            orientation - int - new orientation.
            x - int - current x coordinate of the ship. Not None only during dragging.
            y - int - current y coordinate of the ship. Not None only during dragging.
        """
        self.orientation = orientation
        self.set_rect(x, y)

    def draw(self, rect: pg.Rect = None, rect_width: int = 2) -> None:
        """Draw ship using rect and set color by sunk status.

        Attributes:
            rect - pygame.Rect - rect that represented ship. If None => current ship rect.
            ship_width - int - width of rect.
        """
        if rect is None:
            rect = self.rect
        color = COLORS["RED"] if self.sunk is True else COLORS["BLUE_1"]
        draw_rect(rect, color, rect_width)

    def update_position(self, x: int, y: int, grid: Grid, old_orient: int) -> bool:
        """Update pos list of the ship using coordinates first cell (x, y) and ship's Grid.

        Attributes:
            x - int - x coordinate of first cell in the ship.
            y - int - y coordinate of first cell in the ship.
            grid - Grid - table with this ship.
            old_orient - int - in rollback case rollback orientation of ship on this value.

        Return:
            bool - True if pos list was successfully updated, False otherwise.
        """
        # save old pos list
        old_pos = copy.deepcopy(self.pos)
        for pos in self.pos:
            grid.grid[pos.y][pos.x].set_state(0)
        self.pos = []

        # update pos list
        if self.orientation == 0:
            if all(grid.check_neighbors(x + j, y) and is_in_range(x + j, y)
                   for j in range(self.size)):
                for j in range(self.size):
                    grid.grid[x + j][y].set_state(1)
                    self.add_pos(grid.grid[x + j][y])
                self.set_rect()
                return True
        else:
            if all(grid.check_neighbors(x, y + j) and is_in_range(x, y + j)
                   for j in range(self.size)):
                for j in range(self.size):
                    grid.grid[x][y + j].set_state(1)
                    self.add_pos(grid.grid[x][y + j])
                self.set_rect()
                return True

        # rollback if update didn't apply
        self.pos = copy.deepcopy(old_pos)
        self.orientation = old_orient
        for pos in self.pos:
            grid.grid[pos.y][pos.x].set_state(1)
        self.set_rect()
        return False
