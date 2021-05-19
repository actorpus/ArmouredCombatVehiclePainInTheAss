# updater.py V0.0.3

import hashlib
import sys
import socket
import ssl


def get(url):
    method, url = url.split("://")

    domain, url = url.split("/", 1)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = ssl.wrap_socket(s)

    s.connect((domain, 443 if method == "https" else 80))

    request = b'GET /%s HTTP/1.1\r\nhost: %s\r\n\r\n' % (url.encode(), domain.encode())

    s.send(request)

    headers = {}

    _headers = s.recv(2048)

    for h in _headers.decode().split("\r\n")[1:]:
        if h:
            headers[h.split(": ")[0]] = h.split(": ")[1]

    s.settimeout(5)

    data = b''

    for _ in range((int(headers["Content-Length"]) // 1400) + 2):
        try:
            data += s.read(1400)
        except socket.timeout:
            break

    return data


def replace(_file_name):
    f = get("https://raw.githubusercontent.com/actorpus/TankTrouble/main/" + _file_name)

    with open(_file_name, 'wb') as _file:
        _file.write(f)

    print("UPDATED:", _file_name)


data = get("https://raw.githubusercontent.com/actorpus/TankTrouble/main/VERSIONS")

versions = {}

for v in data.decode().split('\n'):
    versions[v.split(' ')[0]] = v.split(' ')[1]

for file_name in versions.keys():
    try:
        if versions[file_name] != "VOID":
            file = open(file_name, "rb")

            file_contents = file.read()

            if sys.version_info.minor == 9:
                file_hash = hashlib.sha256(file_contents, usedforsecurity=True).hexdigest()
            else:
                file_hash = hashlib.sha256(file_contents).hexdigest()

            if file_hash != versions[file_name]:
                replace(file_name)
            else:
                print("VALID:", file_name)

            file.close()

        else:
            print("IGNORED:", file_name)

    except FileNotFoundError:
        replace(file_name)
