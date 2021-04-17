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

# Define constants
POWERSHELL = 'powershell.exe'

# Functions
def get_world_dirs() -> list:
    """
    Uses the user's username to search for and return a list of directories
    that contain worlds.

    Args:
        None.

    Returns:
        world_dirs: List of directories containing worlds.
    """
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
    """
    Uses a list of world directories to return a list of world names.

    Args:
        world_dirs: List of directories containing worlds.
    
    Returns:
        world_names: List of world names in world_dirs.
    """
    world_names = []
    for i in range(len(world_dirs)):
        f = open(f'{world_dirs[i]}/levelname.txt')
        world_names.append(
            f.readlines()[0]
        )
        f.close()
    return world_names


def pick_world(world_names: list) -> int:
    """
    Prompts the user to pick an enumeration of a world within the given list of
    world names.

    Args:
       world_names: List of world names in world_dirs.

    Returns:
        selection: Int representing user's selected world.
    
    Raises:
        Exception: If user does not input a selection value.
    """
    for i in range(len(world_names)):
        print(f'{i + 1}: {world_names[i]}')
    try:
        selection = input("Enter which Minecraft world you want to serve: ")
    except Exception:
        print("Selecting option 1 by default.")
        selection = 1
    selection = int(selection) - 1
    return selection

def make_volume(world_dirs: list, picked_world: int, volume_name: str) -> None:
    """
    Makes a docker volume of the selected world name's world directory.

    Args:
       world_dirs: List of directories containing worlds.
       picked_world: Int representing user's selected world.
       volume_name: String to name the docker volume.

    Returns:
        None.
    
    Raises:
        Exception: If 'data' is already a directory in this directory.
        Exception: If the volume_name is already used by an existing docker
            volume.
        Exception: If the temporary 'data' directory could not be deleted.
    """
    picked_path = world_dirs[picked_world]
    # Make temporary directory with world information
    tmpdir = os.path.join(os.getcwd(), 'data')
    try:
        shutil.copytree(picked_path, f'{tmpdir}/worlds/Bedrock level')
        shutil.copyfile('server.properties', 'data/server.properties')
    except Exception:
        print("'data' is already a directory. Please remove to have this script function.")
    volumes = subprocess.check_output([
        POWERSHELL,
        'docker volume ls'],
        text = True
            ).replace(" ", "\t"
            ).replace("\n", "\t"
            ).split("\t"
    )
    try:
        subprocess.run([
            POWERSHELL,
            f'docker volume create {volume_name}'
        ])
    except Exception:
        if volume_name in volumes:
            print("Your volume name is already used by an existing volume.")
            decision = input("Do you want to delete your current volume of the same name? (Y/N): ")
            if decision == 'Y':
                try:
                    subprocess.run([
                        POWERSHELL,
                        f'docker volume rm {volume_name}'
                    ])
                except Exception:
                    print("Volume not deleted.")            
            elif decision == 'N':
                print("Volume not deleted.")
        else:
            print("Something went wrong when making your volume.")
    # Add volumes to volume
    subprocess.run([
        POWERSHELL,
        f'docker create -it -v {volume_name}:/data --name file_shipper ubuntu',
    ])
    subprocess.run([
        POWERSHELL,
        'docker cp ./data file_shipper:/',
    ])
    subprocess.run([
        POWERSHELL,
        'docker cp ./data/server.properties file_shipper:/data/server.properties'
    ])
    subprocess.run([
        POWERSHELL,
        'docker rm file_shipper'
    ])
    try:
        shutil.rmtree(tmpdir)
    except Exception:
        print("Something went wrong when trying to delete 'data' directory.")

