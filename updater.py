# updater.py V0.0.3

import requests
import hashlib


def replace(_file_name):
    f = requests.get("https://raw.githubusercontent.com/actorpus/TankTrouble/main/" + _file_name, stream=True)

    if f.status_code == 200:
        with open(_file_name, 'wb') as _file:
            for chunk in f:
                _file.write(chunk)

        print("UPDATED:", _file_name)

data = requests.get("https://raw.githubusercontent.com/actorpus/TankTrouble/main/VERSIONS")

versions = {}

for v in data.text.split('\n'):
    versions[v.split(' ')[0]] = v.split(' ')[1]

for file_name in versions.keys():
    try:
        if versions[file_name] != "VOID":
            file = open(file_name, "rb")

            file_contents = file.read()

            file_hash = hashlib.sha256(file_contents, usedforsecurity=True).hexdigest()

            if file_hash != versions[file_name]:
                replace(file_name)
            else:
                print("VALID:", file_name)

            file.close()

        else:
            print("IGNORED:", file_name)

    except FileNotFoundError:
        replace(file_name)
