"""
    All game settings in dictionary format.
"""

BASE = {
    "WIDTH": 1280,
    "HEIGHT": 800,
    "NAME": "Battleships",
    "USERNAME_LEN": 20
}
USER = {
    "LEFT": 0,
    "RIGHT": 1
}
GRID_PARAMS = {
    "CELL_SIZE": 40,
    "GRID_SIZE": 10,
    "FG_OFFSET": 140,
    "SG_OFFSET": 700
}
FONT_SIZE = {
    "MAIN": 15,
    "WINNER": 60,
    "SET_PHASE": 18,
    "CHAT": 24,
    "USERNAME": 40
}
FONT_NAME = {
    "CHAT": "freesansbold",
    "GAME": "Timesnewroman"
}
COLORS = {
    "WHITE": (255, 255, 255),
    "BLUE0": (128, 166, 206, 128),
    "BLUE_0": (128, 166, 206),
    "BLACK": (0, 0, 0),
    "BLUE_1": (0, 0, 255),
    "RED": (255, 0, 0),
    "GRAY": (128, 128, 128),
    "YELLOW": (255, 204, 0),
    "GREEN": (0, 255, 0)
}
USERNAME_DEST = {
    "LEFT": (300, 550),
    "RIGHT": (900, 550)
}
NETWORK = {
    "SERVER": "10.0.10.48",  # local ip of server!
    "PORT": 5555,
    "MSG_SIZE": 2048 * 10
}
CHAT = {
    "SCROLL_SPEED": 10,
    "MAX_MSG_SIZE": 150
}
