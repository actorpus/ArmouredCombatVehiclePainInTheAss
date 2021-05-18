# client.py V0.1.0
# A valid copy of client.py can be found at https://raw.githubusercontent.com/actorpus/TankTrouble/main/client.py

import hashlib
import math
import pickle
import random
import socket
import pygame
import tkinter as tk
import json
import os


class get_setup:
    def __init__(self, startup, setting_file=".client_settings.json"):
        self.root = tk.Tk()
        self.root.geometry("300x128")
        self.root.title("TankTrouble startup")
        self.root.resizable(False, False)
        # self.root.attributes('-toolwindow', True)

        self.STARTUP = tk.Button(command=self.startup, text="Start Client", justify="left")
        self.ext_startup = startup
        self.setting_file = setting_file

        defaults = self.load_file(setting_file)

        self.widgets = [
            (tk.Entry(self.root, width=18), "IP",
             defaults["IP"] if "IP" in defaults.keys() else "0.0.0.0"
             ),
            (tk.Entry(self.root, width=18), "PORT",
             defaults["PORT"] if "PORT" in defaults.keys() else "3956"
             ),
            (tk.Entry(self.root, width=18), "USERNAME",
             defaults["USERNAME"] if "USERNAME" in defaults.keys() else "Noob321"
             ),
            (tk.Entry(self.root, width=18), "SERVER PASSWORD",
             defaults["SERVER PASSWORD"] if "SERVER PASSWORD" in defaults.keys() else ""
             ),
        ]

        self.colour = (
            tk.Entry(self.root, width=6),
            tk.Entry(self.root, width=6),
            tk.Entry(self.root, width=6)
        )

        self.arrow = tk.IntVar()
        self.arrow.set(defaults["USE_ARROW_KEYS"] if "USE_ARROW_KEYS" in defaults.keys() else 0)

        try:
            for i, colour in enumerate(defaults["COLOUR"]):
                self.colour[i].insert(0, colour)

        except KeyError:
            ...

        self.create_window()

    @staticmethod
    def load_file(file_path) -> dict:
        try:
            with open(file_path, "r") as file:
                return json.load(file)

        except FileNotFoundError:
            ...

        except json.JSONDecodeError:
            ...

        print("\033[31mERROR LOADING CLIENT SETTINGS, PROCEEDING WITH DEFAULTS\033[0m")
        return {}

    def startup(self):
        defaults = {}

        for widget in self.widgets:
            defaults[widget[1]] = widget[0].get()

        defaults["COLOUR"] = [
            int(self.colour[0].get()),
            int(self.colour[1].get()),
            int(self.colour[2].get())
        ]

        defaults["USE_ARROW_KEYS"] = bool(self.arrow.get())

        os.system("attrib -h " + self.setting_file)

        with open(self.setting_file, "w") as file:
            json.dump(defaults, file)

        os.system("attrib +h " + self.setting_file)

        self.root.destroy()

        self.ext_startup(defaults)

    def create_window(self):
        for i, widget in enumerate(self.widgets):
            tk.Label(self.root, text=widget[1]).place(relx=0, y=i * 20, anchor="nw")

            widget[0].place(relx=1, y=i * 20, anchor="ne")
            widget[0].insert(0, widget[2])

        tk.Label(self.root, text="COLOUR").place(relx=0, y=80, anchor="nw")

        self.colour[0].place(relx=1, x=-72, y=80, anchor="ne")
        self.colour[1].place(relx=1, x=-36, y=80, anchor="ne")
        self.colour[2].place(relx=1, y=80, anchor="ne")

        self.STARTUP.place(relx=0.5, rely=1, anchor="s")

        tk.Checkbutton(self.root, text='Use Arrow Keys', variable=self.arrow).place(relx=1, y=100, anchor="ne")

        self.root.mainloop()


def launch_client(settings):
    IP = str(settings["IP"])
    COLOUR = tuple(settings["COLOUR"])
    NAME = str(settings["USERNAME"])
    PORT = int(settings["PORT"])
    WASD = not bool(settings["USE_ARROW_KEYS"])
    PASSWORD = str(settings["SERVER PASSWORD"])

    def gen_map(m):
        m = m.split("\n")[1:]
        d = pygame.surface.Surface((1024, 1024))
        d.fill((255, 255, 255))
        tiles = pygame.image.load("tiles.png")

        for y in range(64):
            for x in range(64):
                if m[y][x] == "#":
                    d.blit(
                        pygame.transform.rotate(tiles.subsurface((32, 0, 16, 16)), random.randint(0, 4) * 90),
                        (x * 16, y * 16))
                    # pygame.draw.rect(d, (0, 0, 0), (x * 16, y * 16, 16, 16))
                elif m[y][x] == "s":
                    d.blit(
                        pygame.transform.rotate(tiles.subsurface((0, 0, 16, 16)), random.randint(0, 4) * 90),
                        (x * 16, y * 16))
                    # pygame.draw.rect(d, (114, 211, 103), (x * 16, y * 16, 16, 16))
                else:
                    d.blit(
                        pygame.transform.rotate(tiles.subsurface((16, 0, 16, 16)), random.randint(0, 4) * 90),
                        (x * 16, y * 16))

        return d

    def draw_tank(_tank):
        power = _tank[4]

        if power == 2:  # shield
            pygame.draw.circle(d, (0, 0, 255), _tank[:2], 20, 2)

        if power == 1:  # sniper
            pygame.draw.line(d, (255, 0, 0), _tank[:2], (
                int(_tank[0] + math.sin(_tank[2] * 0.02463994238) * 1449),
                int(_tank[1] + math.cos(_tank[2] * 0.02463994238) * 1449)
            ))

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

    s.send(pickle.dumps(
        [
            hashlib.sha1(PASSWORD.encode() + s.recv(1024)).digest(),
            COLOUR,
            NAME
        ]
    ))

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

            try:
                data = load(s.recv(65536))
            except ConnectionResetError:
                print("server unexpectedly closed connect")
                return

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


if __name__ == '__main__':
    get_setup(
        startup=launch_client
    )
