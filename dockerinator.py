# The purpose of this script is to copy a user's Minecraft Bedrock Edition's world data into a docker volume.
# This docker volume will be configured to run the world in a container that serves the world.

# import libraries
import os
import shutil
import subprocess
import io
import getpass

# global variables
utf8 = 'utf-8'

# functions

def get_world_dirs() -> list:
    username = getpass.getuser()
    user_path = f'C:\\Users\\{username}\\AppData\\Local\\Packages\\Microsoft.MinecraftUWP_8wekyb3d8bbwe\\LocalState\\games\\com.mojang\\minecraftWorlds'
    world_dirs = []
    for dir in os.listdir(user_path):
        if os.path.isdir(os.path.join(user_path, dir)) == True:
            world_dirs.append(dir)
    for i in range(len(world_dirs)):
        world_dirs[i] = f'{user_path}\{world_dirs[i]}'
    return world_dirs

def get_world_names(world_dirs: list) -> list:
    world_names = []
    for i in range(len(world_dirs)):
        f = open(f'{world_dirs[i]}/levelname.txt')
        world_names.append(
            f.readlines()[0]
        )
        f.close()
    return world_names


def pick_world(world_names: list) -> int:
    for i in range(len(world_names)):
        print(f'{i + 1}: {world_names[i]}')
    selection = input("Enter which Minecraft world you want to serve: ")
    selection = int(selection) - 1
    return selection

def make_volume(
    world_dirs: list, 
    picked_world: int
) -> None:
    picked_path = world_dirs[picked_world]
    # make temporary directory with world information
    tmpdir = os.path.join(os.getcwd(), 'data')
    if 'data' in os.listdir():
        shutil.rmtree(tmpdir)
    shutil.copytree(picked_path, f'{tmpdir}/worlds/Bedrock level')
    shutil.copyfile('server.properties', 'data/server.properties')
    # delete if volume already exists
    volume_name = 'dockerized_world'
    volumes = subprocess.check_output([
        'powershell.exe',
        'docker volume ls'],
        text = True
            ).replace(" ", "\t"
            ).replace("\n", ""
            ).split("\t"
    )
    if volume_name in volumes:
        subprocess.run([
            'powershell.exe',
            f'docker volume rm {volume_name}'
        ])
    # make new volume
    subprocess.run([
        'powershell.exe',
        f'docker volume create {volume_name}'
    ])
    # add volumes to volume
    subprocess.run([
        'powershell.exe',
        'docker create -it -v dockerized_world:/data --name file_shipper ubuntu',
    ])
    subprocess.run([
        'powershell.exe',
        'docker cp ./data file_shipper:/',
    ])
    subprocess.run([
        'powershell.exe',
        'docker cp ./data/server.properties file_shipper:/data/server.properties'
    ])
    subprocess.run([
        'powershell.exe',
        'docker rm file_shipper'
    ])
    shutil.rmtree(tmpdir)

# main
world_dirs = get_world_dirs()
world_names = get_world_names(world_dirs)

world = pick_world(world_names)
print(f'You picked {world_names[world]}.')

make_volume(world_dirs, world)

subprocess.run([
    'powershell.exe',
    'docker run -it -d -e EULA=TRUE -p 19132:19132/udp -v dockerized_world:/data --name dockerized_minecraft itzg/minecraft-bedrock-server'
])



