import pygame

pygame.init()
pygame.font.init()


class menu:
    def __init__(self, w=768, h=432):
        self.w, self.h = w, h

        self.background = pygame.surface.Surface((w, h)).convert_alpha()
        self.background.fill((0, 0, 0, 0))

        pygame.draw.rect(
            self.background,
            (0, 0, 0, 200),
            (0, 0, w, h),
            border_radius=16
        )

        pygame.draw.rect(
            self.background,
            (0, 0, 0, 255),
            (0, 0, w, h),
            8,
            border_radius=16
        )
        pygame.draw.rect(
            self.background,
            (0, 0, 0, 255),
            (0, 0, w, 64),
            8,
            border_radius=16
        )
        pygame.draw.rect(
            self.background,
            (0, 0, 0, 255),
            (0, 56, w // 2, h - 56),
            8,
            border_radius=16
        )
        pygame.draw.rect(
            self.background,
            (0, 0, 0, 255),
            (w // 2 - 8, 56, w // 2 + 8, h - 56),
            8,
            border_radius=16
        )

        self.font_large = pygame.font.Font(
            pygame.font.get_default_font(),
            32
        )
        self.font_small = pygame.font.Font(
            pygame.font.get_default_font(),
            16
        )

        self.background.blit(
            self.font_large.render(
                "ArmouredCombatVehiclePainInTheAss",
                True,
                (255, 255, 255)
            ),
            (16, 16)
        )

    def gen(self, un, kf):
        background = self.background.copy()

        for i, text in enumerate(un):
            background.blit(
                self.font_small.render(
                    "• " + text,
                    True,
                    (255, 255, 255)
                ),
                (16, 72 + (20 * i))
            )

        for i, text in enumerate(kf):
            background.blit(
                self.font_small.render(
                    text,
                    True,
                    (255, 255, 255)
                ),
                (8 + (self.w // 2), 72 + (20 * i))
            )

        return background

    def draw(self, on, un, kf):
        m = self.gen(un, kf)

        on.blit(
            m,
            (
                (on.get_width() - m.get_width()) / 2,
                (on.get_height() - m.get_height()) / 2
            )
        )


display = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
running = True
menu = menu()

r, g, b = 255, 0, 255

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    if b == 255 and g != 255:
        g += 1
        r -= 1
    elif g == 255 and r != 255:
        r += 1
        b -= 1
    elif r == 255 and b != 255:
        b += 1
        g -= 1

    display.fill((int(r), int(g), int(b)))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_TAB]:
        menu.draw(
            display,
            [
                "a",
                "b",
                "c",
                "d.d"
            ],
            [
                "d345 with shotgun",
                "Mre45",
                "Knoe5 with stupidity",
                "Keework",
                "Knogidity",
                "Knogw",
                "Knoead"
            ]
        )

    pygame.display.update()
    clock.tick(60)
