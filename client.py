# client.py V0.0.5
# TankTrouble (c) 2021 by actorpus is licensed under CC BY-NC 4.0. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc/4.0/
# Copy of client.py can be found at https://raw.githubusercontent.com/actorpus/TankTrouble/main/client.py

import socket
import pygame
import pickle
import json
import hashlib

with open("client_config.json", "r") as file:
    data = json.load(file)

IP = data["IP"]
COLOUR = tuple(data["COLOUR"])
NAME = data["NAME"]
PORT = data["PORT"]


def gen_map(m):
    m = m.split("\n")[1:]

    d = pygame.surface.Surface((1024, 1024))

    d.fill((255, 255, 255))

    for y in range(32):
        for x in range(32):
            if m[y][x] != " ":
                pygame.draw.rect(d, (0, 0, 0), (x * 32, y * 32, 32, 32))

    return d


def draw_tank(_tank):
    if _tank[3] in ts.keys():
            r = ts[_tank[3]].copy()
            r = pygame.transform.rotate(r, _tank[2] * 1.41176)
            # pygame.draw.rect(r, (0, 0, 0, 255), (0, 0, r.get_width(), r.get_height()), 1)
            d.blit(r, (_tank[0] - r.get_width() // 2, _tank[1] - r.get_height() // 2))
            # pygame.draw.line(d, (255, 0, 0),
            #                  (_tank[0], _tank[1]),
            #                  ((_tank[0] + math.sin(_tank[2]) * 256, _tank[1] + math.cos(_tank[2]) * 256))
            #                  )

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


def load(data):
    i = 0

    _data = {"bullets": [], "tanks": []}
    nbr_bullets = data[i]

    i += 1

    for _ in range(nbr_bullets):
        _data["bullets"].append(
            (
                int.from_bytes(data[i:i+2], "big"),
                int.from_bytes(data[i+2:i+4], "big")
            )
        )
        i += 4

    nbr_tanks = data[i]

    i += 1

    for _ in range(nbr_tanks):
        _data["tanks"].append(
            (
                # x, y
                int.from_bytes(data[i:i + 2], "big"),
                int.from_bytes(data[i+2:i + 4], "big"),

                # r
                data[i+4],

                # r, g, b
                (
                    data[i+5],
                    data[i+6],
                    data[i+7]
                )
            )
        )

    return _data


d = pygame.display.set_mode((1024, 1024))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c = pygame.time.Clock()
ot = pygame.image.load("tank.png")
ts = {}
s.connect((IP, PORT))

s.send(pickle.dumps([hashlib.sha1(open(__file__, "rb").read() + s.recv(1024), usedforsecurity=True).digest(), COLOUR, NAME]))
vr, background = pickle.loads(s.recv(2048))
print(vr)
if vr[0] == 49: open(__file__, "wb").write(vr[1:])
else:
    background = gen_map(background)

    while not any([_.type == pygame.QUIT for _ in pygame.event.get()]):
        keys = pygame.key.get_pressed()
        s.send(pickle.dumps({
            "w": keys[pygame.K_w],
            "a": keys[pygame.K_a],
            "s": keys[pygame.K_s],
            "d": keys[pygame.K_d],
            "SPACE": keys[pygame.K_SPACE]  # mouse[0]
        }))

        data = load(s.recv(65536))

        print(data)

        d.blit(background, (0, 0))

        for bullet in data["bullets"]:
            draw_bullet(bullet)

        for tank in data["tanks"]:
            draw_tank(tank)

        pygame.display.update()
        c.tick()
        pygame.display.set_caption(str(c.get_fps()))
