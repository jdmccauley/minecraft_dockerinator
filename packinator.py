# The purpose of this script is to automate the archiving and shipment of a Minecraft world volume
# to a remote server.

# Native Libraries
import subprocess

# Custom Libraries
from utils import cloud_utils
from utils import volume_utils

# Define constants
POWERSHELL = 'powershell.exe'

def main() -> None:
    """
    This runs the cloud_utils pack_volume function, which tarballs a docker
    volume. This allows for shipping of the docker volume in archive form.
    """
    #TODO get volume to tar from user
    volumes = volume_utils.get_volumes()
    picked_volume = volume_utils.pick_volume(volumes)
    archive_name = volume_utils.input_archive_name()
    volume_utils.pack_volume(volumes[picked_volume], archive_name)


if __name__ == "__main__":
    main()
