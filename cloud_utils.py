# The purpose of these functions are to automate the archiving and shipment of a Minecraft world volume
# to a remote server.

# Native Libraries
import subprocess

# Functions
def pack_volume(volume_name: str, archive_name: str) -> None:
    subprocess.run([
        'powershell.exe',
        f'docker create -v {volume_name}:/world_volume --name mailman ubuntu /bin/bash'
    ])
    subprocess.run([
        'powershell.exe',
        f'docker run --rm --volumes-from mailman -v ${pwd}:/tar_dir ubuntu tar cvf tar_dir/{archive_name}.tar /world_volume'
    ])
    subprocess.run([
        'powershell.exe',
        'docker rm mailman'
    ])


def unpack_volume(volume_name: str, archive_name: str) -> None:
    subprocess.run([
        'powershell.exe',
        f'docker create -v {volume_name}:/tar_mount --name mail2 ubuntu /bin/bash'
    ])
    subprocess.run([
        'powershell.exe',
        (
            'docker run --rm --volumes-from mail2 -v ${pwd}:/unpacker ubuntu' 
            f'bash -c \"cd /tar_mount && tar xvf /unpacker/{archive_name}.tar --strip 1\"'
        )
    ])
    subprocess.run([
        'powershell.exe',
        'docker rm mail2'
    ])
    
 