"""
    Class represented all ships of one player.
"""
from typing import Generator
from map.grid import Grid
from utils.helper import get_mouse_pos, is_in_range
from ships.ship import Ship


class Fleet:
    """Class represented all ships of one player.

    Attributes:
        offset - int - can be FG_OFFSET or SG_OFFSET (left or right table)
        ships - List[Ship] - List of all ships for player.
        sunk - boolean - True if ship is sunk, False otherwise.
    """
    def __init__(self, offset: int):
        """Initialize one fleet object"""
        self.offset = offset
        self.ships = [[Ship(i, self.offset) for _ in range(5-i)] for i in range(1, 5)]
        self.sunk = False

    def update_offset(self, offset: int) -> None:
        """Set new offset and update offset in all ships of this fleet.

        Attributes:
            offset - int - can be FG_OFFSET or SG_OFFSET (left or right table).
        """
        self.offset = offset
        for ship in self.itr_fleet():
            ship.update_offset(self.offset)

    def is_sunk_fleet(self) -> bool:
        """Check if all ships has sunk attribute on value True.

        Return:
            bool - True if ALL ship is sunk, false otherwise.
        """
        if all(all(ship.sunk is True for ship in ship_type) for ship_type in self.ships):
            self.sunk = True
        return self.sunk

    def itr_fleet(self) -> Generator[Ship, None, None]:
        """Generator for iterating over all ships.

        Return:
            Generator[Ship, None, None] - yield one ship from ships List.
        """
        for ship_type in self.ships:
            for ship in ship_type:
                yield ship

    def draw_ships(self) -> None:
        """Draw all ship on the screen."""
        for ship in self.itr_fleet():
            ship.draw()

    def update_sunk(self, grid: Grid) -> None:
        """Update sunk attribute on all ships using set_sunk method from class Ship.

        Attributes:
            grid - Grid - board with these ships.
        """
        for ship in self.itr_fleet():
            ship.set_sunk(grid)

    def set_dragging(self) -> Ship | None:
        """Check if mouse is on the part of the ship and if is,
           set dragging attribute for this ship to True.

        Return:
            ship - Ship - if mouse is on the part of this ship or None if not.
        """
        row, col = get_mouse_pos()
        if is_in_range(row, col):
            for ship in self.itr_fleet():
                if ship.is_ship_part((col, row)):
                    ship.dragging = True
                    return ship
        return None
