# Battleships

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
