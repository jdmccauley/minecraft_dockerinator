# The purpose of these functions are to automate the archiving and shipment of a Minecraft world volume
# to a remote server.

# Native Libraries
import subprocess

# Functions
def pack_volume() -> None:
    subprocess.run([
        "powershell.exe",
        "docker create -v dockerized_world:/world_volume --name mailman ubuntu /bin/bash"
    ])
    subprocess.run([
        "powershell.exe",
        "docker run --rm --volumes-from mailman -v ${pwd}:/tar_dir ubuntu tar cvf tar_dir/dockerized_world.tar /world_volume"
    ])
    subprocess.run([
        "powershell.exe",
        "docker rm mailman"
    ])


def unpack_volume() -> None:
    subprocess.run([
        "powershell.exe",
        "docker create -v restored_volume:/tar_mount --name mail2 ubuntu /bin/bash"
    ])
    subprocess.run([
        "powershell.exe",
        "docker run --rm --volumes-from mail2 -v ${pwd}:/unpacker ubuntu bash -c \"cd /tar_mount && tar xvf /unpacker/dockerized_world.tar --strip 1\""
    ])
    
 