import pygame
import time

pygame.init()
pygame.mixer.init()

display = pygame.display.set_mode((512, 512))
clock = pygame.time.Clock()
running = True

with open("FireBullet.wav", "rb") as file:
    data = file.read()

sound0 = pygame.mixer.Sound(data)
sound1 = pygame.mixer.Sound("FireBullet.wav")

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_0:
                sound0.play()
            if e.key == pygame.K_1:
                sound1.play()


    pygame.display.update()
    clock.tick(30)
