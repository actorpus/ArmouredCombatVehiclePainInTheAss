# V0.0.1

import requests
import hashlib

# data = requests.get("https://raw.githubusercontent.com/actorpus/TankTrouble/main/client.py")
# print(data.text)

with open("client.py", "rb") as file:
    print(hashlib.sha256(file.read(), usedforsecurity=True).hexdigest())
