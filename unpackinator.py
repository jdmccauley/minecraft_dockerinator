# The purpose of this script is to automate the archiving and shipment of a Minecraft world volume
# to a remote server.

# Custom Libraries
from utils import cloud_utils


def main() -> None:
    """
    This runs the cloud_utils unpack function, which extracts a docker volume
    from a tarball.
    """
    cloud_utils.unpack()


if __name__ == "__main__":
    main()