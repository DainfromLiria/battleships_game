"""
    Class represented a grid that contains cells
"""
from typing import Tuple, Generator
from itertools import product
# utils
from utils.settings import GRID_PARAMS
from utils.helper import is_in_range
# src.map
from map.cell import Cell


class Grid:
    """Class represented a grid that contains Cells

    Attributes:
        grid - list of lists of Cells - represent one grid.
    """
    def __init__(self):
        """Create one grid."""
        self.grid = [[Cell(i, j, 0) for i in range(0, GRID_PARAMS["GRID_SIZE"])]
                     for j in range(0, GRID_PARAMS["GRID_SIZE"])]

    @staticmethod
    def neighbour_iter(x: int, y: int) -> Tuple[int, int]:
        """Generator of neighbouring positions to position with coordinates (x, y).

        Attributes:
            x - int (from 0 to GRID_PARAMS["GRID_SIZE"]-1) - x coordinate.
            y - int (from 0 to GRID_PARAMS["GRID_SIZE"]-1) - y coordinate.

        Return:
            tuple - (new_x, new_y) - neighbour position.
        """
        for i in list(product([0, 1, -1], repeat=2)):
            new_x = x + i[0]
            new_y = y + i[1]
            yield new_x, new_y

    def around_sunk_ship(self, cell: Cell) -> None:
        """Set all empty cells around input cell on state 3 (cell has part of sunk ship).

        Attributes:
            cell - Cell - input cell object.
        """
        x, y = cell.get_coords()
        for new_x, new_y in self.neighbour_iter(x, y):
            if is_in_range(new_x, new_y):
                if self.grid[new_y][new_x].get_state() == 0:
                    self.grid[new_y][new_x].set_state(3)

    def check_neighbors(self, x: int, y: int) -> bool:
        """Check all neighbors of cell on position (x, y).

        Attributes:
            x - int (from 0 to GRID_PARAMS["GRID_SIZE"]-1) - x coordinate.
            y - int (from 0 to GRID_PARAMS["GRID_SIZE"]-1) - y coordinate.

        Return:
            bool - True if around cell is not a ship part, False if is.
        """
        for new_x, new_y in self.neighbour_iter(x, y):
            if is_in_range(new_x, new_y):
                if self.grid[new_x][new_y].get_state() == 1:
                    return False
        return True

    def iter_grid(self) -> Generator[Cell, None, None]:
        """Generator that iterate through all cells on the grid.

        Return:
            Generator[Cell, None, None] - yield Cell object.
        """
        for row in self.grid:
            for cell in row:
                yield cell

    def draw_grid(self, offset: int) -> None:
        """Draw grid by cells.

        Attributes:
            offset - int - can be FG_OFFSET or SG_OFFSET (left or right table).
        """
        for cell in self.iter_grid():
            cell.draw_cell(offset)

    def get_cell_state(self, x: int, y: int) -> int:
        """By input x, y coordinates return state of the cell.

        Attributes:
            x - int - cell's x coordinate.
            y - int - cell's y coordinate.
        Return:
            state - int - cell's state.
        """
        return self.grid[x][y].get_state()

    def set_cell_state(self, x: int, y: int, state: int) -> None:
        """By input x, y coordinates set state of the cell using input state.

        Attributes:
            x - int - cell's x coordinate.
            y - int - cell's y coordinate.
            state - int - cell's new state.
        """
        self.grid[x][y].set_state(state)
