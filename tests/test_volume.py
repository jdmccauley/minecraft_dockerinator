# The purpose of this script is to test volume-related functions.

# Testing on Windows Powershell: `pytest`
# Make sure python is included in the OS' PATH


# Native libraries
import getpass
import os
import subprocess

# Custom libraries
from .. utils import volume_utils

# Define constants
POWERSHELL = 'powershell.exe'

# Tests

def test_get_world_dirs() -> None:
    """
    Tests the volume_utils get_world_dirs function. Runs the function and
    asserts that the output is of type list, and asserts that the list contains
    directories that are valid directories on the host system.
    """
    world_dirs = volume_utils.get_world_dirs()
    assert type(world_dirs) == list, \
        "world_dirs is not of type list."
    for dir in world_dirs:
        assert os.path.isdir(dir), \
            "One or more elements in world_dirs is not a directory path."

def test_get_world_names() -> None:
    """
    Tests the volume_utils get_world_names function. Runs the function and
    asserts that the output is of type list, asserts that the elements of the
    list are of type string, and asserts that the length of the world names
    list is the same length as the world directories list.
    """
    world_dirs = volume_utils.get_world_dirs()
    world_names = volume_utils.get_world_names(world_dirs)
    assert type(world_names) == list, \
        "world_names is not of type list."
    for element in world_names:
        assert type(element) == str, \
            "One or more elements in world_names is not of type string."
    assert len(world_names) == len(world_dirs), \
        "The length of world_names is not the same as world_dirs."

def test_pick_world() -> None:
    """
    Tests the volume_utils pick_world function. Runs the function and asserts
    that the return type is of type int, and that the return value is greater
    than 0.
    """
    world_names = volume_utils.get_world_names(
        volume_utils.get_world_dirs()
    )
    selection = volume_utils.pick_world(world_names)
    assert type(selection) == int, \
        "The selection is not of type int."
    assert selection >= 0, \
        "Not a valid selection value."

def test_make_volume() -> None:
    """
    Tests the volume_utils make_volume function. Asserts that a test docker
    volume name is not present in the list of docker volumes, then runs the
    function. After the function all, this asserts that the test docker volume
    is then included in the list of docker volumes.
    """
    assert 'data' not in os.listdir(), \
        "'data' is already a directory."
    volumes = subprocess.check_output([
        POWERSHELL,
        "docker volume ls"],
        text = True
            ).replace(" ", "\t"
            ).replace("\n", "\t"
            ).split("\t"
    )
    volume_name = 'pytest_test_world'
    assert volume_name not in volumes, \
        "Volume name already exists."
    volume_utils.make_volume(
        volume_utils.get_world_dirs(),
        volume_utils.pick_world(
            volume_utils.get_world_names(
                volume_utils.get_world_dirs()
            )
        ),
        volume_name = volume_name
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
    assert 'data' not in os.listdir(), \
        "'data' directory not deleted."
    # Remove test volume.
    subprocess.run([
        POWERSHELL,
        f'docker volume rm {volume_name}'
    ])

def test_get_volumes() -> None:
    """
    Tests the volume_utils get_volumes function. Asserts that the output is of
    type list, and that it is not empty.
    """
    # TODO assert values by getting with docker module
    volumes = volume_utils.get_volumes()
    assert type(volumes) == list, \
        "The volumes are not returned as type list."
    assert len(volumes) > 0, \
        "The volumes list is empty."


def test_pick_volume() -> None:
    """
    Tests the volume_utils pick_volume function. Asserts that the output is of
    type int, and the default value is 0.
    """
    volumes = volume_utils.get_volumes()
    selection = volume_utils.pick_volume(volumes)
    assert type(selection) == int, \
        "The selection is not of type int."
    assert selection == 0, \
        "The default return value is not 0."

def test_get_archives() -> None:
    """
    Tests the volume_utils get_archives function. Asserts that the output is of
    type list, that the list is not empty, and that a default archive name is
    found in the list. This is achieved by making an
    archive in this test only.
    """
    # Get volumes and make an archive with the default archive name.
    volumes = volume_utils.get_volumes()
    picked_volume = volume_utils.pick_volume(volumes)
    archive_name = volume_utils.input_archive_name()
    volume_utils.pack_volume(volumes[picked_volume], archive_name)
    archives = volume_utils.get_archives()
    test_archive_name = archive_name + ".tar"
    assert type(archives) == list, \
        "The archives are not returned as type list."
    assert len(archives) > 0, \
        "The archives list is empty."
    assert test_archive_name in archives, \
        "Test archive name not found in list of archives."
    # Remove test archive.
    os.remove(test_archive_name)
    

def test_pick_archive() -> None:
    """
    Tests the volume_utils pick_archive function. Asserts that the output is of
    type int, and the default value is 0. This is achieved by making an archive
    in this test only.
    """
    # Get volumes and make an archive with the default archive name.
    volumes = volume_utils.get_volumes()
    picked_volume = volume_utils.pick_volume(volumes)
    archive_name = volume_utils.input_archive_name()
    volume_utils.pack_volume(volumes[picked_volume], archive_name)
    archives = volume_utils.get_archives()
    selection = volume_utils.pick_archive(archives)
    test_archive_name = archive_name + ".tar"
    assert type(selection) == int, \
        "The selection is not of type int."
    assert selection == 0, \
        "The default return value is not 0."
    # Remove test archive.
    os.remove(test_archive_name)

def test_input_archive_name() -> None:
    """
    Tests the volume_utils input_archive_name function. Asserts that the output
    is of type str, and that the default output is value 'archived_world'.
    """
    archive_name = volume_utils.input_archive_name()
    assert type(archive_name) == str, \
        "The archive name is not of type str."
    assert archive_name == "archived_world", \
        "The default output is not 'archived_world'."

def test_input_volume_name() -> None:
    """
    Tests the volume_utils input_volume_name function. Asserts that the output
    is of type str, and that the default output is value 'extrated_volume'.
    """
    volume_name = volume_utils.input_volume_name()
    assert type(volume_name) == str, \
        "The volume name is not of type str."
    assert volume_name == "extracted_volume", \
        "The default output is not 'extracted_volume'."
