"""
    Unit tests for game.
"""
import subprocess
import pygame as pg
import pytest

# for network test (don't work on gitlab ci)
# import os
# import pyautogui
# from online.network import Network

from map.cell import Cell
from map.grid import Grid
from ships.ship import Ship
from player.player import Player
from utils.settings import GRID_PARAMS, BASE
from utils.helper import get_rect, is_in_range


def test_codestyle():
    """Test codestyle by PEP8.
        R0902: Too many instance attributes (10/7) (too-many-instance-attributes)
        R0801: Similar lines in 2 files
        E1101: Module 'pygame' has no 'QUIT' member (no-member)
    """
    command = "pylint ./**/*.py --disable=R0902,R0801,E1101"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True, check=False)
    result_list = result.stdout.split('\n')[1:-5]
    assert len(result_list) == 0, "Project has PEP8 errors."


@pytest.mark.parametrize(
    'x, y, state, set_state, expected',
    [
        (0, 0, 0, 2, ((0, 0), 2)),
        (1, 0, -1, 3, ((1, 0), 3)),
        (9, 0, 2, -1, ((9, 0), -1)),
        (0, 9, 4, 0, ((0, 9), 0)),
    ])
def test_cell(x, y, state, set_state, expected):
    """Test for class Cell."""
    cell = Cell(x, y, state)
    cell.set_state(set_state)
    assert cell.get_state() == expected[1]
    assert cell.get_coords() == expected[0]


def test_grid():
    """Test for Grid class."""
    grid = Grid()
    grid.set_cell_state(0, 0, 4)
    grid.around_sunk_ship(Cell(0, 0, 4))
    assert grid.get_cell_state(0, 0) == 4
    assert grid.get_cell_state(0, 1) == 3
    assert grid.get_cell_state(1, 0) == 3
    assert grid.get_cell_state(1, 1) == 3
    grid.set_cell_state(0, 0, 1)
    assert grid.get_cell_state(0, 0) == 1
    assert grid.check_neighbors(0, 0) is False
    assert grid.check_neighbors(5, 5) is True


def test_ship():
    """Test for Ship class."""
    # create grid
    grid = Grid()
    c_size = GRID_PARAMS["CELL_SIZE"]
    # create ships
    ship = Ship(2, GRID_PARAMS["FG_OFFSET"])
    ship.add_pos(Cell(0, 0, 1))
    ship.add_pos(Cell(1, 0, 1))
    ship2 = Ship(2, GRID_PARAMS["FG_OFFSET"])
    ship2.add_pos(Cell(3, 0, 1))
    ship2.add_pos(Cell(4, 0, 1))
    # add data about ships on grid
    grid.set_cell_state(0, 0, 1)
    grid.set_cell_state(1, 0, 1)
    grid.set_cell_state(3, 0, 1)
    grid.set_cell_state(4, 0, 1)
    # create rect for both ships
    ship.set_rect()
    ship2.set_rect()
    # tests is_ship_part
    assert ship.is_ship_part((0, 0)) is True
    assert ship.is_ship_part((1, 0)) is True
    assert ship.is_ship_part((3, 0)) is False
    assert ship2.is_ship_part((4, 0)) is True
    # test update_offset
    assert ship.rect == get_rect(GRID_PARAMS["FG_OFFSET"], (0, 0), (c_size, c_size * 2))
    ship.update_offset(GRID_PARAMS["SG_OFFSET"])
    assert ship.rect == get_rect(GRID_PARAMS["SG_OFFSET"], (0, 0), (c_size, c_size * 2))
    # test update_position and set_orientation
    ship.set_orientation(1)
    assert ship.update_position(0, 8, grid, 0) is True
    assert ship.rect == get_rect(GRID_PARAMS["SG_OFFSET"], (8, 0), (c_size * 2, c_size))
    assert ship2.update_position(0, 8, grid, 0) is False


def test_fleet():
    """Tests for Fleet class."""
    player = Player(0)
    player.random_set_ships()
    fleet = player.fleet
    assert fleet.is_sunk_fleet() is False
    for ship in fleet.itr_fleet():
        ship.sunk = True
    assert fleet.is_sunk_fleet() is True
    assert fleet.offset == GRID_PARAMS["FG_OFFSET"]
    for ship in fleet.itr_fleet():
        assert ship.offset == GRID_PARAMS["FG_OFFSET"]
    fleet.update_offset(GRID_PARAMS["SG_OFFSET"])
    assert fleet.offset == GRID_PARAMS["SG_OFFSET"]
    for ship in fleet.itr_fleet():
        assert ship.offset == GRID_PARAMS["SG_OFFSET"]
    pg.init()
    pg.display.set_mode((BASE["WIDTH"], BASE["HEIGHT"]))
    assert fleet.set_dragging() is None


@pytest.mark.parametrize(
    'x, y, expected',
    [
        (0, 0, True),
        (1, 0, True),
        (-1, 0, False),
        (10, 0, False),
    ])
def test_is_in_range(x, y, expected):
    """Test for helper function is_in_range."""
    assert is_in_range(x, y) == expected


# only if server is DOWN
# def test_negative_network():
#     """Negative test for Network class. Cannot connect to the server."""
#     net = Network()
#     assert net.connected is False


# only if server is UP
# def test_positive_network():
#     """Positive test and negative if user more than two."""
#     os.system("python server.py")
#     net2 = Network()
#     assert net2.connected == 0
#     net3 = Network()
#     assert net3.connected == 1
#     net4 = Network()
#     assert net4.connected is False
#     pyautogui.hotkey('ctrl', 'c')
