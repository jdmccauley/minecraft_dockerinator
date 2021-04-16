# The purpose of this script is to automate the archiving and shipment of a Minecraft world volume
# to a remote server.

# Custom Libraries
from utils import cloud_utils

def main():
    cloud_utils.pack_volume()


if __name__ == "__main__":
    main()