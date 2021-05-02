# V0.0.1

import requests
import hashlib


def replace(_file_name):
    f = requests.get("https://raw.githubusercontent.com/actorpus/TankTrouble/main/" + _file_name)

    if f.text != "404: Not Found":
        with open(_file_name, "w") as nf:
            nf.write(f.text)

        print("Updated", _file_name)
    else:
        print("Could not update", _file_name)


data = requests.get("https://raw.githubusercontent.com/actorpus/TankTrouble/main/VERSIONS")

versions = {}

for v in data.text.split('\n'):
    versions[v.split(' ')[0]] = v.split(' ')[1:]

print(versions)

for file_name in versions.keys():
    try:
        file = open(file_name, "rb")

        file_contents = file.read()

        print(file_contents.split(b'\n')[0].split(b' ')[2].decode())

        print(hashlib.sha256(file_contents, usedforsecurity=True).hexdigest())

        file.close()

    except FileNotFoundError:
        replace(file_name)

