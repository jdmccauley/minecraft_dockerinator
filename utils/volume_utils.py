# The purpose of these functions are to copy a user's Minecraft Bedrock Edition's world data into a docker volume.
# This docker volume will be configured to run the world in a container that serves the world.

# Native Libraries
import os
import shutil
import subprocess
import io
import getpass
import glob

# Global variables
utf8 = 'utf-8'

# Define constants
POWERSHELL = 'powershell.exe'
EXCEPTION = "Selecting option 1 by default."

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
        print(EXCEPTION)
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

def get_volumes() -> list:
    """
    Makes a list of docker volumes and returns it.

    Args:
        None.
    
    Returns:
        volumes: List of unique docker volumes.
    """
    volumes = subprocess.check_output([
        POWERSHELL,
        'docker volume ls'],
        text = True
            ).replace(" ", "\t"
            ).replace("\n", "\t"
            ).split("\t"
    )
    name_index = volumes.index("NAME")
    volumes = volumes[name_index + 1:]
    # Remove repeated value elements.
    volumes = list(set(volumes))
    # Remove empty  elements.
    volumes.remove("")
    return volumes

def pick_volume(volumes: list) -> int:
    """
    Prompts the user to pick an enumeration of a docker volume within the given
    list of volume names.

    Args:
       volumes: List of docker volumes.

    Returns:
        selection: Int representing user's selected volume.
    
    Raises:
        Exception: If user does not input a selection value.
    """
    for i in range(len(volumes)):
        print(f'{i + 1}: {volumes[i]}')
    try:
        selection = input("Enter which volume you want to use: ")
    except Exception:
        print(EXCEPTION)
        selection = 1
    selection = int(selection) - 1
    return selection

def get_archives() -> list:
    """
    Makes a list of tarballs and returns it.

    Args:
        None.
    
    Returns:
        archive_list: List of tarballs in the current directory.
    """
    archives_list = glob.glob("*.tar")
    return archives_list

def pick_archive(archives: list) -> int:
    """
    Prompts the user to pick an enumeration of a tarball within a list of
    given tarballs.

    Args:
       archives: List of tarballs.

    Returns:
        selection: Int representing user's selected tarball.
    
    Raises:
        Exception: If user does not input a selection value.
    """
    for i in range(len(archives)):
        print(f'{i + 1}: {archives[i]}')
    try:
        selection = input("Enter which archive you want to use: ")
    except Exception:
        print(EXCEPTION)
        selection = 1
    selection = int(selection) - 1
    return selection


def input_archive_name() -> str:
    """
    Gets input from the user regarding a name for an archive.

    Args:
        None.
    
    Returns:
        archive_name: Name for the archive.
    
    Raises:
        Exception: If user does not input a name for the archive.
    """
    try:
        archive_name = input("Enter a name for your volume archive: ")
    except Exception:
        print("Using archive name 'archived_world' by default.")
        archive_name = "archived_world"
    return archive_name

def input_volume_name() -> str:
    """
    Gets input from the user regarding a name for a docker volume.

    Args:
        None.
    
    Returns:
        volume_name: Name for the docker volume.
    
    Raises:
        Exception: If user does not input a name for the docker volume.
    """
    try:
        volume_name = input("Enter a name for your volume to make: ")
    except Exception:
        print("Using volume name 'extracted_archive' by deault.")
        volume_name = "extracted_volume"
    return volume_name

def pack_volume(volume_name: str, archive_name: str) -> None:
    """
    This takes a docker volume name and name for a tarball, and then tarballs
    the docker volume into a tarball named after the given name. The process
    is achieved by using an intermediate docker container named 'mailman'.

    Args:
        volume_name: Name of volume to tarball.
        archive_name: Name of tarball to be named 'archive_name.tar'.
    
    Returns:
        None.
    """
    subprocess.run([
        POWERSHELL,
        f'docker create -v {volume_name}:/world_volume --name mailman ' +
            'ubuntu /bin/bash'
    ])
    subprocess.run([
        POWERSHELL,
        'docker run --rm --volumes-from mailman -v ${pwd}:/tar_dir ubuntu ' +
            f'tar cvf tar_dir/{archive_name}.tar /world_volume'
    ])
    subprocess.run([
        POWERSHELL,
        'docker rm mailman'
    ])


def unpack_volume(volume_name: str, archive_name: str) -> None:
    """
    This takes a docker volume name and a name of a tarball, and extracts the
    tarball into a docker container named after the given docker volume name.
    This process is achieved by using an intermediate docker container named
    'mail2'.

    Args:
        volume_name: Name of volume to make.
        archive_name: Name of tarball to extract, without the '.tar' extension.
    
    Returns:
        None.
    """
    subprocess.run([
        POWERSHELL,
        f'docker create -v {volume_name}:/tar_mount --name mail2 ' +
            'ubuntu /bin/bash'
    ])
    subprocess.run([
        POWERSHELL,
        (
            'docker run --rm --volumes-from mail2 -v ${pwd}:/unpacker ubuntu ' 
            'bash -c \"cd /tar_mount && tar xvf ' +
                f'/unpacker/{archive_name}.tar --strip 1\"'
        )
    ])
    subprocess.run([
        POWERSHELL,
        'docker rm mail2'
    ])
