# The purpose of this script is to copy a user's Minecraft Bedrock Edition's world data into a docker volume.
# This docker volume will be configured to run the world in a container that serves the world.

# Native Libraries
import subprocess

# Custom Libaries
from utils import volume_utils

def main():
    world_dirs = volume_utils.get_world_dirs()
    world_names = volume_utils.get_world_names(world_dirs = world_dirs)

    world = volume_utils.pick_world(world_names = world_names)
    print(f'You picked {world_names[world]}.')

    try:
        volume_name = input("Enter a name for your world volume: ")
    except:
        print("Naming the volume 'dockerized_world' by default.")
        volume_name = 'dockerized_world'

    volume_utils.make_volume(world_dirs = world_dirs, picked_world = world, volume_name = volume_name)

    # Start server with volume

    subprocess.run([
        'powershell.exe',
        'docker run -it -d -e EULA=TRUE -p 19132:19132/udp -v dockerized_world:/data --name dockerized_minecraft itzg/minecraft-bedrock-server'
    ])


if __name__ == "__main__":
    main()
