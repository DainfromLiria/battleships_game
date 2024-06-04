"""
    Main for player.
"""
import pygame as pg

from utils.settings import BASE
from menus.main_menu import MainMenu


def main():
    """Begin game proces, draw window and main menu."""
    pg.init()
    pg.display.set_mode((BASE["WIDTH"], BASE["HEIGHT"]))
    pg.display.set_caption(BASE["NAME"])
    menu = MainMenu()
    menu.run()


if __name__ == '__main__':
    main()
