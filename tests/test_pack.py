# The purpose of this script is to test volume-related tarring and un-tarring functions.

# Native Libraries
import os
import subprocess

# Custom libraries
from .. utils import volume_utils
from .. utils import cloud_utils

# Define constants
POWERSHELL = 'powershell.exe'

# Tests

def test_pack():
    """
    Tests the volume_utils and cloud_utils functions for packing a volume. This
    creates a test volume and tarballs the volume, asserts that the tarball was
    created, the deletes the volume.
    """
    volume_name = 'pytest_test_volume'
    packed_volume = 'pytest_test_world'
    volume_archive = 'pytest_test_world.tar'
    assert volume_archive not in os.listdir(), \
        "'pytest_test_world.tar' already in directory."
    volume_utils.make_volume(
        volume_utils.get_world_dirs(),
        volume_utils.pick_world(
            volume_utils.get_world_names(
                volume_utils.get_world_dirs()
            )
        ),
        volume_name = volume_name
    )
    volume_utils.pack_volume(
        volume_name = volume_name,
        archive_name = packed_volume
    )
    assert volume_archive in os.listdir(), \
        "'pytest_test_world.tar' not created in directory."
    # Right now doesn't actually delete.
    subprocess.run([
        POWERSHELL,
        f'docker volume rm {volume_name}'
    ])

def test_unpack():
    """
    Tests a tarball for it's ability to be unpacked and used as a docker
    volume. A volume is created with the tarball content, asserts that the
    volume was made, then the volume is deleted.
    """
    packed_volume = 'pytest_test_world.tar'
    volume_name = 'pytest_restored_volume'
    volumes = subprocess.check_output([
        POWERSHELL,
        "docker volume ls"],
        text = True
            ).replace(" ", "\t"
            ).replace("\n", "\t"
            ).split("\t"
    )
    assert volume_name not in volumes, \
        "'pytest_restored_volume' already in volume list."
    volume_utils.unpack_volume(
        volume_name = volume_name,
        archive_name = packed_volume
    )
    volumes = subprocess.check_output([
        POWERSHELL,
        "docker volume ls"],
        text = True
            ).replace(" ", "\t"
            ).replace("\n", "\t"
            ).split("\t"
    )
    assert volume_name in volumes, \
        "Volume not created."
    subprocess.run([
        POWERSHELL,
        f'docker volume rm {volume_name}'
    ])
    os.remove(packed_volume)
