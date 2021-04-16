# The purpose of this script is to test volume-related tarring and un-tarring functions.

# Native Libraries
import os
import subprocess

# Custom libraries
import volume_utils
import cloud_utils

# Tests

def test_pack():
    volume_name = 'pytest_test_volume'
    packed_volume = 'pytest_test_world.tar'
    assert packed_volume not in os.listdir(), "'pytest_test_world.tar' already in directory."
    volume_utils.make_volume(
        volume_utils.get_world_dirs(),
        volume_utils.pick_world(
            volume_utils.get_world_names(
                volume_utils.get_world_dirs()
            )
        ),
        volume_name = volume_name
    )
    cloud_utils.pack_volume(volume_name = volume_name, archive_name = packed_volume)
    assert packed_volume in os.listdir(), "'pytest_test_world.tar' not created in directory."
    subprocess.run([
        'powershell.exe',
        f'docker volume rm {volume_name}'
    ])

def test_unpack():
    packed_volume = 'pytest_test_world.tar'
    volume_name = 'pytest_restored_volume'
    volumes = subprocess.check_output([
        "powershell.exe",
        "docker volume ls"],
        text = True
            ).replace(" ", "\t"
            ).replace("\n", "\t"
            ).split("\t"
    )
    assert volume_name not in volumes, "'pytest_restored_volume' already in volume list."
    cloud_utils.unpack_volume(volume_name = volume_name, archive_name = packed_volume)
    volumes = subprocess.check_output([
        "powershell.exe",
        "docker volume ls"],
        text = True
            ).replace(" ", "\t"
            ).replace("\n", "\t"
            ).split("\t"
    )
    assert volume_name in volumes, "Volume not created."
    subprocess.run([
        'powershell.exe',
        f'docker volume rm {volume_name}'
    ])

