# The purpose of this script is to serve a minecraft world from a volume.

# Native libraries
import subprocess

# Custom libraries
from utils import volume_utils

def main() -> None:
    """
    Serves a minecraft world from a volume.
    """
    volumes = volume_utils.get_volumes()
    picked_volume = volumes[volume_utils.pick_volume(volumes)]
    # Start server with volume.
    subprocess.run([
        'powershell.exe',
        'docker run -it -d -e EULA=TRUE -p 19132:19132/udp -v ' +
        f'{picked_volume}:/data --name dockerized_minecraft ' +
        'itzg/minecraft-bedrock-server'
    ])

if __name__ == "__main__":
    main()
