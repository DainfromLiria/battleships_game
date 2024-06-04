"""
    Class represented one player.
"""
import random
import pygame as pg
# utils
from utils.settings import USER, GRID_PARAMS
# src
from ships.fleet import Fleet
from map.grid import Grid


class Player:
    """Class represented one player.

    Attributes:
        id - int - must be USER["LEFT"] or USER["RIGHT"] (0 or 1).
        offset - int - can be FG_OFFSET or SG_OFFSET (left or right table).
        board - Grid - players board.
        fleet - Fleet - players fleet.
        username - str - players username (Default is User + (0 or 1))
    """
    def __init__(self, player_id: int, username: str = "User"):
        """Create one Player object."""
        self.id = player_id
        if self.id == USER["LEFT"]:
            self.offset = GRID_PARAMS["FG_OFFSET"]
        else:
            self.offset = GRID_PARAMS["SG_OFFSET"]
        self.board = Grid()
        self.fleet = Fleet(self.offset)
        self.username = username + str(self.id)

    def invert_player(self) -> None:
        """Invert offset in all ships in fleet."""
        self.fleet.update_offset(self.offset)

    def reset(self) -> None:
        """Reset board and fleet. Generate new disposition of ships."""
        self.board = Grid()
        self.fleet = Fleet(self.offset)
        self.random_set_ships()

    def draw(self) -> None:
        """Draw board, fleet status and for left player fleet."""
        self.draw_status()
        self.board.draw_grid(self.offset)
        if self.id == USER["LEFT"]:
            self.fleet.draw_ships()

    def draw_status(self) -> None:
        """Draw fleet status for this player."""
        start_y = 150
        start_x = 8 if self.id == USER["LEFT"] else 1130
        cnt_type = 0
        for ship_type in self.fleet.ships:
            cnt_ship = 0
            for ship in ship_type:
                rect = pg.Rect(start_x + (cnt_ship * ship.size), start_y + cnt_type,
                               15 * ship.size, 15)
                ship.draw(rect, 1)
                cnt_ship += 20
            cnt_type += 25

    def random_set_ships(self) -> None:
        """Create random distribution of ships on the board.
        In first step randomly select orientation for ship. Then generate random
        coordinates (x, y) and try to set this ships. If position is not valid,
        generate new orientation and coordinates. Else set this ship on positions on the board.
        """
        for i in range(1, 5):
            size = i
            count = 5 - size
            while count > 0:
                direction = random.randint(0, 1)
                if direction == 0:
                    x = random.randint(0, 10 - size)
                    y = random.randint(0, 9)
                    if all(self.board.check_neighbors(x + j, y) for j in range(size)):
                        for j in range(size):
                            self.board.grid[x + j][y].set_state(1)
                            self.fleet.ships[i - 1][count - 1].add_pos(self.board.grid[x + j][y])
                        self.fleet.ships[i - 1][count - 1].set_orientation(direction)
                        count -= 1
                else:
                    x = random.randint(0, 9)
                    y = random.randint(0, 10 - size)
                    if all(self.board.check_neighbors(x, y + j) for j in range(size)):
                        for j in range(size):
                            self.board.grid[x][y + j].set_state(1)
                            self.fleet.ships[i - 1][count - 1].add_pos(self.board.grid[x][y + j])
                        self.fleet.ships[i - 1][count - 1].set_orientation(direction)
                        count -= 1

    def get_cell_state(self, x: int, y: int) -> int:
        """By input x, y coordinates return state of the cell.

        Attributes:
            x - int - cell's x coordinate.
            y - int - cell's y coordinate.
        Return:
            state - int - cell's state.
        """
        return self.board.get_cell_state(x, y)

    def set_cell_state(self, x: int, y: int, state: int) -> None:
        """By input x, y coordinates set state of the cell using input state.

        Attributes:
            x - int - cell's x coordinate.
            y - int - cell's y coordinate.
            state - int - cell's new state.
        """
        self.board.set_cell_state(x, y, state)
