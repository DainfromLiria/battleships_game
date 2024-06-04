[![battleships_tests](https://github.com/DainfromLiria/battleships_game/actions/workflows/python-package.yml/badge.svg)](https://github.com/DainfromLiria/battleships_game/actions/workflows/python-package.yml)
# Battleships

### About
This is a multiplayer 2D game for two players developed in Python using the `pygame` library. The game represents the classic tabletop game Battleships with default rules. More information can be found on the [wiki](https://en.wikipedia.org/wiki/Battleship_(game)).

This game is my university semester project for the BI-PYT subject in the academic year 2023/2024.



### How run this game
* Install all library's and packages

>[NOTE] Server and players machines must have already installed python 3.11 or higher.

```shell 
pip install -r requirements.txt
```
* Go to `app` folder.

```shell
cd app
```
* Run server in the terminal. 
>[NOTE] Before run the server change ip address in `utils/settings.py`. Use `ipconfig` for Windows or
`ifconfig` for Linux to find LAN ip of machine on which server runs and set it in `NETWORK` settings in `utils/settings.py`. 
Both players must set the same ip in their settings file. This version of game has been tested only in LAN using two pc! 

```shell
python server.py
```
* Run clients on other terminal or other pc.

```shell
python main.py
```
