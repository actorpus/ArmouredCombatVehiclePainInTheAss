# client.pyw V0.1.0
# A valid copy of client.pyw can be found at https://raw.githubusercontent.com/actorpus/TankTrouble/main/client.py

import base64
import hashlib
import json
import math
import os
import pickle
import random
import socket
import ssl
import sys
import tkinter as tk

import pygame


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

        self.update = tk.Button(command=update, text="update", justify="left")

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
        self.update.place(relx=0, rely=1, anchor="sw")

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
        tiles = "1pWsB{R9L33IzNk4f!Yl{RIH_90uf55xz7D*9!pt1OomA0sjO5{saL00|5R5w~cbOifz1?f3bmIt$S9feqgtbbGMChvxa7`d{?xG" \
                "XtRcAx|4gbfLyePXSR!O3J3=j4GJC+4Idm6ARiPUAQd1Q6d)51ArcQC5)U657$6%NAR8GV8yOxM7aS500{sI9`2ivG3<mg22Ifrx" \
                "^cMj94FdHw2Hzk6^$h{_1p)j60R996^#csj0Ri^{x|4dZep#@8T(N>-vWRQ7l!35>WUqf-q;*lPdRDWAWwVxpvx;u7eq6STZm)h?" \
                "000061Opim4Idm89v>AQ9TgcC6&@21AQBH96AvF77#$fG9T^uL85ax+2?PQG0{H_X;sH3#043uU6|fr#*#!Xo2LS#b0Q?>R^EnF9" \
                "7X<MJ1pEdI(*hlt01MRtvxQ`$b5EprTdjv~vxQ}_ep;n<QlN8DoNr5_b5FC1ZlZNnq;*iHc2uu@SFwR!000020Ra^b3?CU58y6W6" \
                "4;2s%6&er{9}*865)T~~6crH<6%h{=5f1?X000000rmqH&jcy61rp;b2Hz9{^a2Rq5CQi?0Q*e=@@oszM+)B#4D1jE>L>}-1_Ag3" \
                "rg>Pdd{(iAWu|vlrg>SSb5EyxTd8?grgc!Da!!_POr~~JuYFgqeOI%DWVelR3Izlb3I`q&5FZy692OWA6Brc~7aJ589TE;15)c*@" \
                "6BiQ@7ZVT{6A%ms1p)y80R003?+6dw9s&420R9;W;1?LE6A9Qa0_!~p-AMxOSPAJM62Te}#6Jb=Cjk8erg>PeeOI-KYqEo4t$SCk" \
                "eqN<@QmJ=Ssd!Ycep;k~YOjJ~sd-hYcvP~4W3`HHArcND6Am8|4j&Q^926256ciQ|6dDy08xs=~5fT#;5*HB?7ZDN{5fU8}4;v2*" \
                "0R9C7>JbdcA_M6h0Q?^V?oJTGJqOxC5WX)LsTT+09uV{u4bTV>#TpII1_Jd1wTf-8ep#!7XsU>FuZC-}f?%(GSfq7Pt9)9rgk!IQ" \
                "W3PW)sdrSYfMK|gb+LkAA`=cG6AvE}4i^s>6%Y~_6cZQ}5*!s192OWC6B-o~78?{68x$5B6c!*C6de;00Q(FH+%^r*QU~5S0Q@Wf" \
                "{4N9SL<ZeR5WqeVz%c{x5EA?%1nLwJ!UGku0S4v*tbt>xcvZKOd7pDts(xUygJH3NU72l6uzy>sgKDOIVYP~FopDj4b5O8;TCss&" \
                "A`=fI6b~8@7Z42^4GIzz5fl~_6B`v19TyiK6&M{76dx579~BfI6%-*F7akZF0`dkB#UK&FKLzPa0R2h<_$vw7DFN<d2i{r&>}v(*" \
                "EDY^80QpG+?-dB*0tM><t9@LneO#}7SFD6-wT^SFeOj)6UaoyxlW0e#dRn1%RjYhkqjgfNdRMP~SG0&~A`=fG6Av2_5f&5{6%rE{" \
                "6A~5_6dM&29~c)O78D;75Fiy1AQcfH6%ipB7abWG55fQ$rv(_V4+H5H0QoBm);b!Z5DL~K1n3t8=qM7t4idy71Mo8d`VR=<0v5CY" \
                "ta?<XbyBc@TeOI2v4LKsePN(-Po;HHu6$OmeOjn_SE6%IsdrPbfLyPBS+j*@A`=fG6Av5{5Em5`7#0*56%!W~6dM*49TgND6BQQ_" \
                "4;~T^9uf~85)U5|5E&H}9+Chap#%}m1pxH~1nD6Q&@&Ih6a(-G0R003^$iQxDhk^{0rw*T_5%*d0v(zFt$J0ZbyBi}W3Yf-vV>!%" \
                "dReA-Rk4C!uYFgkcT<;bO{jNLsCQDbi*c=gUbv8UA`=fG6AvB}4;mE`92XQB784j26c`p18WI!}4;T^<5El^;7ZDH_5fC2|5E~Q{" \
                "8l?ap(-Q;s1_1dc1M5l-$S4Ni3Ig{73El$(@C5?)9Rm3;0R0RB`~w5=0}9y!uY6arfnK3@SFeI$rg~hYcv`Q2U8#a-k7h=!d|07!" \
                "PpNrUuZC%zbyl5nQn7+yArlWF6Av8{4;K#?7ZDO05)K{|5gZc`91|875hD{26B`v38x<8B6%`*85g-!}3FiVH^b`v05&-*D0Q*@3" \
                "?I{5J6b0xg7pnyh$^roP2mt>a0Q(gM>IDek0s;C1uY6apeOH)nQLlw*xQ}(QfnTzOW3-5Bs(4eceOI!AVXS~*t%GH;fnJ($P_Tbn" \
                "ArlWF77`f|8w?2=4GI+*5Dy^}4<Hl}9~c)N7#<xL7abNB9TpZH78V~B5+M^04EY2k-2x!I2@2#y0Q)ik{}cfJI{^D-2H`3M?jr#E" \
                "836u81MWH!ya*So0SDs)uYOsbc3QE4UbBT}s(4eIa8a*)Sgw3ku6tFme_OJIWV426w~cYIfLyD3SFe3oAruiH7#15977+~>4h<3+" \
                "5f2{|4<Hi{AQlrJ7Ze>A6&)579TpTF78Dp15gii`3i$&d*8n1|0TjX%2ki;~{tE#99{~L^0QW8h>QMpsDgga00Q)Qi>j?+p0|EI1" \
                "r-EvzfMl?MT(*mDs(V_kdsnZ0SFL<lta?<lhGx2wd8>Y2t9)9od{(b~R<nj?ArlWE7Ze{E791258Wj>A91|WE6Cf579~TrH7!?>7" \
                "6&Mv17!?#46%-T`5*HE>0{sIC@BtFc01w6h4et>E`XvPHItA$z2IdkIx*Z7K4FUTK0RIXB{{;a51OWX6v50M(aZ|2=VYQ2Jl4(n&" \
                "c2ll=R-|=MrFK)Wep;$}R+VW<sd-kfd{?rBWV(}jAQKNE6A&O46CD>4A0HGS9~B=T6(1TG9~l=P85bNG7Zwy778Dy66dMl?6cY~@" \
                "0R962`~w2@0|fB{7W*Rw>oyG3O%uEr4%r71yaov00|EO40sjO8{{{g61OWX5uZ?%5dRwP~Xs?1|uzy>zfL^YARkMX;uYFgtgJQFW" \
                "XRv=;uzp&veOI=OZ@iX%9up5B6AvE~4;>m3ARrYVAQc}U6(1H99u*TH8W<oO866oL9T^)P85<Q79uf}`"

        tiles = base64.b85decode(tiles)
        tiles = pygame.image.fromstring(tiles, (48, 16), "RGB")

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
    ot = b'|NsC0|NlNdK0ZD^K0ZD^K0ZD^K0ZD^K0ZD^K0ZD^K0ZD^K0ZD^K0g2d|NsC0|Ns9!K0ZD^K0ZD^K0ZD^K0ZD^K0ZD^K0ZD^K0ZD^K0ZD^K' \
         b'0ZD^K0ZD^KL7v!0000!K0ZD^K0ZD^K0ZD^K0ZD^K0ZD^K0ZD^K0ZD^K0ZD^K0ZD^K0ZD^J^%m!0000!K0ZD^K0ZD^d3kwxd3kwxd3kwxd3' \
         b'kwxd3kwxd3kwxK0ZD^K0ZD^J^%m!0000!K0ZD^K6!b0d3kwxd3kwxd3kwxd3kwxd3kwxd3kwxd3kw0K0ZD^J^%m!0000!K0ZD^K6!b0d3k' \
         b'wxd3kwxd3kwxd3kwxd3kwxd3kwxd3kw0K0ZD^J^%m!0000!K0ZD^K6!b0d3kwxd3kwxd3kwxd3kwxd3kwxd3kwxd3kw0K0ZD^J^%m!0000' \
         b'!K0ZD^K6!b0d3kwxd3kwxd3kwxd3kwxd3kwxd3kwxd3kw0K0ZD^J^%m!0000!K0ZD^K6!b0d3kwxd3kwxd3kwxd3kwxd3kwxd3kwxd3kw0' \
         b'K0ZD^J^%m!0000!K0ZD^K6!b0d3kwxd3kwxd3kwxd3kwxd3kwxd3kwxd3kw0K0ZD^J^%m!0000!K0ZD^K6!b0d3kwxd3kwxd3kwxd3kwxd' \
         b'3kwxd3kwxd3kw0K0ZD^J^%m!0000!K0ZD^K6!b0d3kwxd3kwxd3kwxd3kwxd3kwxd3kwxd3kw0K0ZD^J^%m!0000!K0ZD^K6!b0d3kwxd3' \
         b'kwxd3kwxd3kwxd3kwxd3kwxd3kw0K0ZD^J^%m!0000!K0ZD^K6!b0d3kwxd3kwxd3kwxd3kwxd3kwxd3kwxd3kw0K0ZD^J^%m!0000!K0Z' \
         b'D^K6!b0d3kwxd3kwxd3kwxd3kwxd3kwxd3kwxd3kw0K0ZD^J^%m!0000!K0ZD^K6!b0d3kwxd3kwxd3kwxd3kwxd3kwxd3kwxd3kw0K0ZD' \
         b'^J^%m!0000!K0ZD^K6!b0d3kwxd3kwxd3kwxd3kwxd3kwxd3kwxd3kw0K0ZD^J^%m!0000!K0ZD^K0ZD^d3kwxd3kwxd3kwxd3kwxd3kwx' \
         b'd3kwxK0ZD^K0ZD^J^%m!0000!K0ZD^K0ZD^K0ZD^K0bMQd3kwxd3kwxd3ioQK0ZD^K0ZD^K0ZD^J^%m!0000!K0ZD^K0ZD^K0ZD^K0bMQd' \
         b'3kwxd3kwxd3ioQK0ZD^K0ZD^K0ZD^J^%m!0000!K0ZD^K0ZD^K0ZD^K0bMQd3kwxd3kwxd3ioQK0ZD^K0ZD^K0ZD^J^%m!0000!K0ZD^K0' \
         b'ZD^K0ZD^K0bMQd3kwxd3kwxd3ioQK0ZD^K0ZD^K0ZD^J^%m!0000!K0ZD^K0ZD^K0ZD^K0bMQd3kwxd3kwxd3ioQK0ZD^K0ZD^K0ZD^J^%' \
         b'm!0000!K0ZD^K0ZD^K0ZD^K0bMQd3kwxd3kwxd3ioQK0ZD^K0ZD^K0ZD^J^%m!|Ns9!K0ZD^K0ZD^K0ZD^K0bMQd3kwxd3kwxd3ioQK0ZD' \
         b'^K0ZD^K0ZD^KL7v!|NsC0|NlNdK0ZD^K0ZD^K0bMQd3kwxd3kwxd3ioQK0ZD^K0ZD^K0g2d|NsC0|NsC0|NsC0|NsC0|NsC0|NnV;d3kwx' \
         b'd3kwxd3pc;|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NnV;d3kwxd3kwxd3pc;|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|' \
         b'NsC0|NnV;d3kwxd3kwxd3pc;|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NnV;d3kwxd3kwxd3pc;|NsC0|NsC0|NsC0|NsC0|N' \
         b'sC0|NsC0|NsC0|NsC0|NnV;d3kwxd3kwxd3pc;|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|9N?Nd3kyN|NsC0|NsC0|Ns' \
         b'C0|NsC0|NsC0'
    p = b'000010RaI40RaI40RaI40RaI40RR9100000000000000000000000000000000000000000000000000000000000000000000000000000' \
        b'00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' \
        b'00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' \
        b'0000000000000000000000000000000000000000000000960|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Ns' \
        b'C0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC00001>?Ej$b' \
        b'|Df#upzQyk?Ej$b|Df#upzQyk?Ej$b|Df#upzQwu000000HEyupzQyk?Ej$b|Df#upzQyk?Ej$b|Df#upzQyk?Ej$b{{R300001>?Ej$b|D' \
        b'f#upzQyk?Ej$b|Df#upzQyk?Ej$b|Df#upzQwu000000HEyupzQyk?Ej$b|Df#upzQyk?Ej$b|Df#upzQyk?Ej$b{{R300001>?Ej$b|Df#' \
        b'upzQyk?Ej$b|Df#upzQyk?Ej$b|Df#upzQwu000000HEyupzQyk?Ej$b|Df#upzQyk?Ej$b|Df#upzQyk?Ej$b{{R300001>?Ej$b|Df#up' \
        b'zQyk?Ej$b|Df#upzQyk?Ej$b|Df#upzQwu00960|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Ns' \
        b'C0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC00001>?Ej$b|Df#u00000' \
        b'00000000000001>?Ej$b|Df#upzQwu000000HEyupzQxlOiWBnOiWBnOiWBnOiWBnOiWBnOiWCm?Ej$b{{R300001>?Ej$b|Df#upzQyk?E' \
        b'j$b|Df#upzQyk?Ej$b|Df#upzQwu000000HEyupzQyk?Ej$b|Df#uHo_=2!YH8Z|Df#upzQyk?Ej$b{{R300001>?Ejt@7oHavo);IO?Ej$' \
        b'b|Df#upzQyk?Ej$b|Df#upzQwu000000HEyupzQyk?Ej$b|Df#upzQyk?Ej$b|Df#upzQyk?Ej$b{{R300001>?Ej$b|Df#upzQyk?Ej$b|' \
        b'7&Y&pzQyk?Ej$b|Df#upzQwu00960|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Ns' \
        b'C0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC00001>?Ej$b{{R30AHwP%!s-A303X8Y' \
        b'AHwPY005xu|Df#upzQwu000000HEyuOiWCMhK7cQhK7cQOiWBnOiYG`hK7cQhK7brOiZBc{{R300001>?Ej$b|Df#upzQyi7Z;uv7oHavo)' \
        b';IO?Ej$b|Df#upzQwu000000HEyupzQyk?Ej$b|2D!XHo_=2!YDSvD4^{BpzQyk?Ej$b{{R300001>?Ejt@7oHavo);JY|No%u|Df#upzQy' \
        b'k?Ej$b|Df#upzQwu000000HEyupzQyk?Ej$b|Df#upzQyk?Ej$b|Df#upzQyk?Ej$b{{R300001>?Ej$b|Df#upzQyk?Eh<PYoP4^pzQyk?' \
        b'Ej$b|Df#upzQwu00960|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Ns' \
        b'C0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC00001>?Ee4&03X8YAHwP%!s-A303X8YAHwP%!s-A3' \
        b'0HEyupzQwu000000HEyuOiWCMhK7cQhK7cQOiWBnOiYG`hK7cQhK7brOiZBc{{R300001>?Ej$b|Df#upzQyi7Z;uv7oHavo);IO?Ej$b|D' \
        b'f#upzQwu000000HEyupzQyk?Ef~xC^o_<Ho_=2!YDSvC^o_<pzQyk?Ej$b{{R300001>?Ejt@7oHav|NsC0|NovB7ohC_pzQyk?Ej$b|Df#' \
        b'upzQwu000000HEyupzQyk?Ej$b|Df#upzQyk?Ej$b|Df#upzQyk?Ej$b{{R300001>?Ej$b|Df#upzQyk?Eh<PYoP4^pzQyk?Ej$b|Df#up' \
        b'zQwu00960|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Ns' \
        b'C0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC00001>?Ee4&03X8YAHwP%!s-A303X8YAHwP%!s-A30HEyupzQwu' \
        b'000000HEyuOiWBnOiWBnOiWBnOiWBnOiWBnOiWBnOiWBnOiZBc{{R300001>?Ej$b|Df#upzQyi7Z;uv7oHavo);IO?Ej$b|Df#upzQwu00' \
        b'0000HEyupzQxP!YDSvC^o_<pzQyk?Ef~xC^o_<Ho_>N?Ej$b{{R300001>?Ej$b|NsC0|NsA<7Z;uv7ytkNpzQyk?Ej$b|Df#upzQwu0000' \
        b'00HEyupzQyk?Ej$b|Df#upzQyk?Ej$b|Df#upzQyk?Ej$b{{R300001>?Ej$b|Df#upzQwu0000000000pzQyk?Ej$b|Df#upzQwu00960|' \
        b'NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Ns' \
        b'C0sHmugg@ynB|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC00001>?Ee4&0000000000000000000000000000000HEyupzQwu000000HEyu' \
        b'OiWBnOiWBnOiWBnOiWBnOiWBnOiWBnOiWBnOiZBc{{R300001>?Ej$b|Df#upzQyi7Z;uv7oHavo);IO?Ej$b|Df#upzQwu000000HEyupz' \
        b'QxP!YDSvD4^{BpzQyk?Ej$b|2D!XHo_>N?Ej$b{{R300001>?Ej$b|Df#uo);IM7Z?Bk|NsC0o);IO?Ej$b|Df#upzQwu000000HEyupzQy' \
        b'k?Ej$b|DG2Yo);IM7Z;uv7ohC_pzQyk?Ej$b{{R300001>?Ej$b|Df#u00030|Nj60000000001>?Ej$b|Df#upzQwu00960|NsC0|NsC0|' \
        b'NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0g@uIx009' \
        b'60|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC00001>?Ee4&03X8YAHwP%!s-A303X8YAHwP%!s-A30HEyupzQwu000000HEyuOiWCMhK7cQ' \
        b'hK7cQOiWBnOiYG`hK7cQhK7brOiZBc{{R300001>?Ej$b|Df#upzQyi7Z;uv7oHavo);IO?Ej$b|Df#upzQwu000000HEyupzQyk?Ej$b|D' \
        b'f#uHo_=2!YH8Z|Df#upzQyk?Ej$b{{R300001>?Ej$b|Df#upzQzu|NsC0|DG2Yo);JY|No%u|Df#upzQwu000000HEyupzQxeW<y10Lq%p' \
        b'oMP@@qW<y10Lq%poMP@^w?Ej$b{{R300001>?Ej$b{{R30|Ns90000000000000000005xu|Df#upzQwu00960|NsC0|NsC0|NsC0|NsC0|' \
        b'NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Ns' \
        b'C0|NsC0|NsC0|NsC0|NsC0|NsC00001>?Ee4&03X8YAHwP%!s-A303X8YAHwP%!s-A30HEyupzQwu000000HEyuOiWCMhK7cQhK7cQOiWBn' \
        b'OiYG`hK7cQhK7brOiZBc{{R300001>?Ej$b|Df#upzQyi7Z;uv7oHavo);IO?Ej$b|Df#upzQwu000000HEyupzQyk?Ej$b|2D!XHo_=2!Y' \
        b'DSvD4^{BpzQyk?Ej$b{{R300001>?Ej$b|Df#upzQyk?Ejt@7oHav|NsC0|No%u|Df#upzQwu000000HEyupzQxeW<y10Lq%poMP@@qW<y1' \
        b'0Lq%poMP@^w?Ej$b{{R300001>?Ej$b{{R30|Ns90000000000000000005xu|Df#upzQwu00960|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|' \
        b'NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Ns' \
        b'C0|NsC0|NsC0|NsC00001>?Ej$b{{R30AHwP%!s-A303X8YAHwPY005xu|Df#upzQwu000000HEyupzQxlOiYG`hK7cQOiWBnOiYG`hK7cQ' \
        b'OiWCm?Ej$b{{R300001>?Ej$b|Df#upzQzAyiC!&Owqhd(Y#Ec?Ej$b|Df#upzQwu000000HEyupzQyk?Ef~xC^o_<Ho_=2!YDSvC^o_<pz' \
        b'Qyk?Ej$b{{R300001>?Ej$b|Df#upzQyk?Ej$b|NsC0|Ns9?OiZBc|Df#upzQwu000000HEyupzQyk?Ej$b|Df#upzQyk?Ej$b|Df#upzQy' \
        b'k?Ej$b{{R300001>?Ej$b{{R3000000000000000000000005xu|Df#upzQwu00960|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|' \
        b'NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Ns' \
        b'C0|NsC00001>?Ej$b|Df#u0000000000000000001>?Ej$b|Df#upzQwu000000HEyupzQxlOiWBnOooPrOiWBnOiYG`hD=OMOiWCm?Ej$b' \
        b'{{R300001>?Ej$b|Df#upzQzAyiC!&Owqhd(Y#Ec?Ej$b|Df#upzQwu000000HEyupzQxP!YDSvC^o_<pzQyk?Ef~xC^o_<Ho_>N?Ej$b{{' \
        b'R300001>?Ej$b|Df#upzQyk?Ej$b|Df#upzQyk?Eg$mOrY%lpzQwu000000HEyupzQyk?Ej$b|Df#upzQyk?Ej$b|Df#upzQyk?Ej$b{{R3' \
        b'00001>?Ej$b|Df#u0000000000000000001>?Ej$b|Df#upzQwu00960|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|' \
        b'NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0000' \
        b'1>?Ej$b|Df#upzQyk?Ej$b|Df#upzQyk?Ej$b|Df#upzQwu000000HEyupzQyk?Ej$b|4d9wOiWBnOiWBnOrY%lpzQyk?Ej$b{{R300001>' \
        b'?Ej$b|Df#upzQyk?Ej$b|Df#upzQyk?Ej$b|Df#upzQwu000000HEyupzQxP!YDSvD4^{BpzQyk?Ej$b|2D!XHo_>N?Ej$b{{R300001>?E' \
        b'j$b|Df#upzQyk?Ej$b|Df#upzQyk?Ej$b|4d9wpzQwu000000HEyupzQyk?Ej$b|Df#upzQyk?Ej$b|Df#upzQyk?Ej$b{{R300001>?Ej$' \
        b'b|Df#upzQwu0000000000pzQyk?Ej$b|Df#upzQwu00960|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|' \
        b'NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC00001>?Ej$b|Df' \
        b'#upzQyk?Ej$b|Df#upzQyk?Ej$b|Df#upzQwu000000HEyupzQyk?Ej$b|Df#upzQyk?Ej$b|Df#upzQyk?Ej$b{{R300001>?Ej$b|Df#u' \
        b'pzQyk?Ej$b|Df#upzQyk?Ej$b|Df#upzQwu000000HEyupzQyk?Ej$b|Df#upzQyk?Ej$b|Df#upzQyk?Ej$b{{R300001>?Ej$b|Df#upz' \
        b'Qyk?Ej$b|Df#upzQyk?Ej$b|Df#upzQwu000000HEyupzQyk?Ej$b|Df#upzQyk?Ej$b|Df#upzQyk?Ej$b{{R300001>?Ej$b|Df#upzQy' \
        b'k?Ej$b|Df#upzQyk?Ej$b|Df#upzQwu00960|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|' \
        b'NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC000000000000000000000000' \
        b'00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' \
        b'00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' \
        b'00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' \
        b'00000000000000000000000960|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|' \
        b'NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0'

    ot = base64.b85decode(ot)
    ot = pygame.image.fromstring(ot, (16, 32), "RGB")
    p = base64.b85decode(p)
    p = pygame.image.fromstring(p, (140, 14), "RGB")
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


def update():
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


if __name__ == '__main__':
    get_setup(
        startup=launch_client
    )