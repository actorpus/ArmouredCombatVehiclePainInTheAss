import hashlib
import os

print("".join([(file + " " * (len(max(os.listdir(), key=lambda _: len(_))) - len(file)) + ":" + hashlib.sha256(open(file, "rb").read(), usedforsecurity=True).hexdigest() + "\n") if file[0] != "." and "." in file else "" for file in os.listdir()]))
