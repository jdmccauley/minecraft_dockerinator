# Welcome to the
               _                            __ _   
     _ __ ___ (_)_ __   ___  ___ _ __ __ _ / _| |_
    | '_ ` _ \| | '_ \ / _ \/ __| '__/ _` | |_| __|
    | | | | | | | | | |  __/ (__| | | (_| |  _| |_
    |_| |_| |_|_|_| |_|\___|\___|_|  \__,_|_|  \__|

         _            _             _             _
      __| | ___   ___| | _____ _ __(_)_ __   __ _| |_ ___  _ __
     / _` |/ _ \ / __| |/ / _ \ '__| | '_ \ / _` | __/ _ \| '__|
    | (_| | (_) | (__|   <  __/ |  | | | | | (_| | || (_) | |
     \__,_|\___/ \___|_|\_\___|_|  |_|_| |_|\__,_|\__\___/|_|

    
[![Generic badge](https://img.shields.io/badge/tests-passing-brightgreen)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/coverage-67%25-yellowgreen)](https://shields.io/)
# Quickstart

```
python3 make_volume.py
python3 serve_volume.py
```

# Purpose

The purpose of this repo is to automate the migration of an existing world in Minecraft Bedrock Edition to a Docker volume. This way, the volume can be mounted to a container that serves [Minecraft Bedrock Edition.](https://hub.docker.com/r/itzg/minecraft-bedrock-server)

This python script finds your Minecraft worlds on your PC, lets you pick which one to convert to a volume, and copies it to a Docker volume. This can then be run with the server container to host your Minecraft world.

# Supported OS'es

* Windows 10

# Dependencies

* Minecraft Bedrock Edition 

* [Minecraft Bedrock Server Docker container by itzg](https://hub.docker.com/r/itzg/minecraft-bedrock-server)

* Docker

* Python3

# Assumptions

* World is saved on a C drive at it's default location, as per [source](https://gaming.stackexchange.com/questions/330407/where-does-minecraft-for-windows-10-store-its-data):
```
C:\Users\username\AppData\Local\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\minecraftWorlds
```


# Steps:

1. Clone this repo.
2. Turn your world into a docker volume by running `python3 make_volume.py`
3. Serve your world from the volume with `python3 serve_volume.py`.
4. Open Minecraft, go to 'Play -> Friends -> LAN Games -> Dedicated Server'
5. Play Minecraft with your friends (or alone, that's fun too)!

# Testing:

Run tests and get test coverage by running `python3 test.py`.

Note that this depends on `pytest` and `coverage`, so install those with `pip3 install pytest coverage` before testing.

# Advanced Use:

This repository can also be used to pack docker volumes into archives and send them to servers. To do so:
1. Make a volume with `python3 make_volume.py`.
2. Archive the volume with `python3 pack_volume.py`.
3. Send the volume to your server.
4. Unpack the volume on your server with `python3 unpack_volume.py`.
    * Note that this is currently only supported for Windows servers at this time since the script uses powershell.
5. Serve your world from the volume with `python3 serve_volume.py`.

# Side Notes:

Windows Python versions can be confusing. If `python3` is installed from the 'Microsoft Store', all pip installs might need to be done with:
```
python3 -m pip install <package_name>
```
