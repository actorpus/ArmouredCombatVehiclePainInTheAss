# client.py V0.0.6
# A valid copy of client.py can be found at https://raw.githubusercontent.com/actorpus/TankTrouble/main/client.py

import hashlib
import json
import pickle
import socket
import sys

import pygame

try:
    with open("client_config.json", "r") as file:
        data = json.load(file)
except FileNotFoundError:
    with open("client_config.json", "w") as file:
        file.write('{\n  "NAME": "put your name/username here",\n  "IP": "ip of the server goes here",\n  '
                   '"PORT": port of the server goes here [INT],\n  "COLOUR": [\n    1,\n    0,\n    0,\n    '
                   '"3 [FLOAT] values between 0 and 1 (represent R, G, B) \n  ]\n}')
        print("ERROR non existent config")
        print("please fill client_config.json")
        sys.exit()

IP = str(data["IP"])
COLOUR = tuple(data["COLOUR"])
NAME = str(data["NAME"])
PORT = int(data["PORT"])
WASD = not bool(data["USE_ARROW_KEYS"])


def gen_map(m):
    m = m.split("\n")[1:]
    d = pygame.surface.Surface((1024, 1024))
    d.fill((255, 255, 255))

    for y in range(64):
        for x in range(64):
            if m[y][x] == "#":
                pygame.draw.rect(d, (0, 0, 0), (x * 16, y * 16, 16, 16))
            elif m[y][x] == "s":
                pygame.draw.rect(d, (114, 211, 103), (x * 16, y * 16, 16, 16))

    return d


def draw_tank(_tank):
    power = _tank[4]

    if power == 2:  # shield
        pygame.draw.circle(d, (0, 0, 255), _tank[:2], 20, 2)

    if _tank[3] in ts.keys():
        r = ts[_tank[3]].copy()
        r = pygame.transform.rotate(r, _tank[2] * 1.41176)
        d.blit(r, (_tank[0] - r.get_width() // 2, _tank[1] - r.get_height() // 2))

    else:
        new_image = pygame.surface.Surface((ot.get_width(), ot.get_height())).convert_alpha()

        for x in range(ot.get_width()):
            for y in range(ot.get_height()):
                p = ot.get_at((x, y))

                if ot.get_at((x, y))[0] == 255:
                    new_image.set_at((x, y), (0, 0, 0, 0))
                else:
                    new_image.set_at((x, y), (_tank[3][0] * p[0] // 255, _tank[3][1] * p[0] // 255, _tank[3][2] * p[0] // 255, 255))

        ts[_tank[3]] = new_image


def draw_bullet(_bullet):
    pygame.draw.circle(d, (0, 0, 0), _bullet, 2)


def draw_powerup(_powerup):
    d.blit(p, (_powerup[0] + 1, _powerup[1] + 1), ((14 * (_powerup[2] - 1)), 0, 14, 14))


def load(data):
    i = 0

    _data = {"bullets": [], "tanks": [], "powerups": []}

    nbr_bullets = data[i]

    i += 1

    for _ in range(nbr_bullets):
        _data["bullets"].append((int.from_bytes(data[i:i + 2], "big"), int.from_bytes(data[i + 2:i + 4], "big")))
        i += 4

    nbr_powerups = data[i]

    i += 1

    for _ in range(nbr_powerups):
        _data["tanks"].append(
            (
                # x, y
                int.from_bytes(data[i:i + 2], "big"),
                int.from_bytes(data[i + 2:i + 4], "big"),
                # r
                data[i + 4],
                # r, g, b
                (
                    data[i + 5],
                    data[i + 6],
                    data[i + 7]
                ),
                # powerup
                data[i + 8]
            )
        )

        i += 9

    nbr_powerups = data[i]

    i += 1

    for _ in range(nbr_powerups):
        _data["powerups"].append(
            (
                # x, y
                int.from_bytes(data[i: i + 2], "big"),
                int.from_bytes(data[i + 2: i + 4], "big"),
                # type
                data[i + 4]
            )
        )

        i += 5

    return _data


def dump(w, a, s, d, SPACE):
    return (
            (w << 0) +
            (a << 1) +
            (s << 2) +
            (d << 3) +
            (SPACE << 4)
    ).to_bytes(1, 'big')


d = pygame.display.set_mode((1024, 1024))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c = pygame.time.Clock()
ot = pygame.image.load("tank.png")
p = pygame.image.load("powerups.png")
ts = {}
s.connect((IP, PORT))

s.send(pickle.dumps([hashlib.sha1(open(__file__, "rb").read() + s.recv(1024)).digest(), COLOUR, NAME]))
vr, background = pickle.loads(s.recv(8192))
print(vr[1:])
if vr[0] == 49:
    open(__file__, "wb").write(vr[1:])
else:
    background = gen_map(background)

    while not any([_.type == pygame.QUIT for _ in pygame.event.get()]):
        keys = pygame.key.get_pressed()
        s.send(dump(
            w=keys[pygame.K_w] if WASD else keys[pygame.K_UP],
            a=keys[pygame.K_a] if WASD else keys[pygame.K_LEFT],
            s=keys[pygame.K_s] if WASD else keys[pygame.K_DOWN],
            d=keys[pygame.K_d] if WASD else keys[pygame.K_RIGHT],
            SPACE=keys[pygame.K_SPACE]
        ))

        data = load(s.recv(65536))

        d.blit(background, (0, 0))

        for bullet in data["bullets"]:
            draw_bullet(bullet)

        for tank in data["tanks"]:
            draw_tank(tank)

        for powerup in data["powerups"]:
            draw_powerup(powerup)

        pygame.display.update()
        c.tick()
        pygame.display.set_caption(str(c.get_fps()))
