# The purpose of this script is to automate the archiving and shipment of a Minecraft world volume
# to a remote server.

# Custom Libraries
from utils import cloud_utils
from utils import volume_utils


def main() -> None:
    """
    This runs the cloud_utils unpack function, which extracts a docker volume
    from a tarball.
    """
    # TODO: get volume and archive from user
    archive_list = volume_utils.get_archives()
    archive_name = archive_list[volume_utils.pick_archive(archive_list)]
    # Remove the .tar
    archive_name = archive_name.split(".tar")[0]
    volume_name = volume_utils.input_volume_name()
    volume_utils.unpack_volume(volume_name, archive_name)


if __name__ == "__main__":
    main()
