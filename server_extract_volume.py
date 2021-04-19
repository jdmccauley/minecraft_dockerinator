# The purpose of this script is to extract a volume from a server.

import docker

def main() -> None:
    """
    Main.
    """
    client = docker.from_env()
    minecraft_container = client.containers.get("dockerized_minecraft")
    archive_name = input("Enter a name for the archive: ") + ".tar"
    bits, stat = minecraft_container.get_archive("/data")
    f = open(archive_name, 'wb')
    for chunk in bits:
        f.write(chunk)
    f.close()

if __name__ == "__main__":
    main()
