# The purpose of this script is to automate the archiving and shipment of a Minecraft world volume
# to a remote server.

# Custom Libraries
from utils import cloud_utils

def main() -> None:
    """
    This runs the cloud_utils pack_volume function, which tarballs a docker
    volume. This allows for shipping of the docker volume in archive form.
    """
    cloud_utils.pack_volume()


if __name__ == "__main__":
    main()
