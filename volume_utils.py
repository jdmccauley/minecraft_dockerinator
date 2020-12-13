# The purpose of these functions are to copy a user's Minecraft Bedrock Edition's world data into a docker volume.
# This docker volume will be configured to run the world in a container that serves the world.

# Native Libraries
import os
import shutil
import subprocess
import io
import getpass

# Global variables
utf8 = 'utf-8'

# Functions
def get_world_dirs() -> list:
    username = getpass.getuser()
    user_path = (f'C:\\Users\\{username}\\AppData\\Local\\Packages\\'
        'Microsoft.MinecraftUWP_8wekyb3d8bbwe\\LocalState\\'
        'games\\com.mojang\\minecraftWorlds'
    )
    world_dirs = []
    for dir in os.listdir(user_path):
        if os.path.isdir(os.path.join(user_path, dir)) == True:
            world_dirs.append(dir)
    for i in range(len(world_dirs)):
        world_dirs[i] = f'{user_path}/{world_dirs[i]}'
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
    try:
        selection = input("Enter which Minecraft world you want to serve: ")
    except:
        print("Selecting option 1 by default.")
        selection = 1
    selection = int(selection) - 1
    return selection

def make_volume(world_dirs: list, picked_world: int) -> None:
    picked_path = world_dirs[picked_world]
    # Make temporary directory with world information
    tmpdir = os.path.join(os.getcwd(), 'data')
    try:
        shutil.copytree(picked_path, f'{tmpdir}/worlds/Bedrock level')
        shutil.copyfile('server.properties', 'data/server.properties')
    except:
        print("'data' is already a directory. Please remove to have this script function.")
    try:
        volume_name = input("Enter a name for your world volume: ")
    except:
        print("Naming the volume 'dockerized_world' by default.")
        volume_name = 'dockerized_world'
    volumes = subprocess.check_output([
        'powershell.exe',
        'docker volume ls'],
        text = True
            ).replace(" ", "\t"
            ).replace("\n", "\t"
            ).split("\t"
    )
    try:
        subprocess.run([
            'powershell.exe',
            f'docker volume create {volume_name}'
        ])
    except:
        if volume_name in volumes:
            print("Your volume name is already used by an existing volume.")
            decision = input("Do you want to delete your current volume of the same name? (Y/N): ")
            if decision == 'Y':
                try:
                    subprocess.run([
                        'powershell.exe',
                        f'docker volume rm {volume_name}'
                    ])
                except:
                    print("Volume not deleted.")            
            elif decision == 'N':
                print("Volume not deleted.")
        else:
            print("Something went wrong when making your volume.")
    # Add volumes to volume
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
    try:
        shutil.rmtree(tmpdir)
    except:
        print("Something went wrong when trying to delete 'data' directory.")
    return volume_name


