# The purpose of this script is to test volume-related functions.

# Testing on Windows Powershell: `pytest`
# Make sure python is included in the OS' PATH


# Native libraries
import getpass
import os
import subprocess

# Custom libraries
import volume_utils

# Tests

def test_get_world_dirs():
    world_dirs = volume_utils.get_world_dirs()
    assert type(world_dirs) == list, "world_dirs is not of type list."
    for dir in world_dirs:
        assert os.path.isdir(dir), "One or more elements in world_dirs is not a directory path."

def test_get_world_names():
    world_dirs = volume_utils.get_world_dirs()
    world_names = volume_utils.get_world_names(world_dirs)
    assert type(world_names) == list, "world_names is not of type list."
    for element in world_names:
        assert type(element) == str, "One or more elements in world_names is not of type string."
    assert len(world_names) == len(world_dirs), "The length of world_names is not the same as world_dirs."

def test_pick_world():
    world_names = volume_utils.get_world_names(
        volume_utils.get_world_dirs()
    )
    selection = volume_utils.pick_world(world_names)
    assert type(selection) == int, "The selection is not of type int."
    assert selection >= 0, "Not a valid selection value."

def test_make_volume():
    assert 'data' not in os.listdir(), "'data' is already a directory."
    volumes = subprocess.check_output([
        "powershell.exe",
        "docker volume ls"],
        text = True
            ).replace(" ", "\t"
            ).replace("\n", "\t"
            ).split("\t"
    )
    volume_name = 'test_world'
    assert volume_name not in volumes, "Volume name already exists."
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
        "powershell.exe",
        "docker volume ls"],
        text = True
            ).replace(" ", "\t"
            ).replace("\n", "\t"
            ).split("\t"
    )
    assert volume_name in volumes, "Volume not created."
    assert 'data' not in os.listdir(), "'data' directory not deleted."

