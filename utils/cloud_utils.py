# The purpose of these functions are to automate the archiving and shipment of a Minecraft world volume
# to a remote server.

# Native Libraries
import subprocess
import os

# Define Constants
POWERSHELL = 'powershell.exe'

# Functions
def pack_volume(volume_name: str, archive_name: str) -> None:
    """
    This takes a docker volume name and name for a tarball, and then tarballs
    the docker volume into a tarball named after the given name. The process
    is achieved by using an intermediate docker container named 'mailman'.

    Args:
        volume_name: Name of volume to tarball.
        archive_name: Name of tarball to be named 'archive_name.tar'.
    
    Returns:
        None.
    """
    subprocess.run([
        POWERSHELL,
        f'docker create -v {volume_name}:/world_volume --name mailman ' +
            'ubuntu /bin/bash'
    ])
    subprocess.run([
        POWERSHELL,
        'docker run --rm --volumes-from mailman -v ${pwd}:/tar_dir ubuntu ' +
            f'tar cvf tar_dir/{archive_name}.tar /world_volume'
    ])
    subprocess.run([
        POWERSHELL,
        'docker rm mailman'
    ])


def unpack_volume(volume_name: str, archive_name: str) -> None:
    """
    This takes a docker volume name and a name of a tarball, and extracts the
    tarball into a docker container named after the given docker volume name.
    This process is achieved by using an intermediate docker container named
    'mail2'.

    Args:
        volume_name: Name of volume to make.
        archive_name: Name of tarball to extract, without the '.tar' extension.
    
    Returns:
        None.
    """
    subprocess.run([
        POWERSHELL,
        f'docker create -v {volume_name}:/tar_mount --name mail2 ' +
            'ubuntu /bin/bash'
    ])
    subprocess.run([
        POWERSHELL,
        (
            'docker run --rm --volumes-from mail2 -v ${pwd}:/unpacker ubuntu' 
            'bash -c \"cd /tar_mount && tar xvf ' +
                f'/unpacker/{archive_name}.tar --strip 1\"'
        )
    ])
    subprocess.run([
        POWERSHELL,
        'docker rm mail2'
    ])
    
 