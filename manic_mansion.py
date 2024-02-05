import pygame as pg
import sys
import random

WIDTH = 800  # Bredden til vinduet
HEIGHT = 800  # Høyden til vinduet

# Størrelsen til vinduet
SIZE = (WIDTH, HEIGHT)

# Frames Per Second (bilder per sekund)
FPS = 60

# Farger (RGB)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (100, 100, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

sauer = []
hindringer = []

# Initiere pygame
pg.init()

# Lager en overflate (surface) vi kan tegne på
surface = pg.display.set_mode(SIZE)
pg.display.set_caption("Manic Mansion")
clock = pg.time.Clock()

run = True

class SpillObjekt:
    def __init__(self, x, y, width, height, color):
        self.rect = pg.Rect(x, y, width, height)
        self.color = color

    def tegn(self, surface):
        pg.draw.rect(surface, self.color, self.rect)

class Menneske(SpillObjekt):
    def __init__(self, x, y, width, height, color, speed: int):
        super().__init__(x, y, width, height, color)
        self.speed = speed

    def plassering(self):
        if self.rect.x + self.rect.width > WIDTH:
            self.rect.x = WIDTH - self.rect.width
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y + self.rect.height > HEIGHT:
            self.rect.y = HEIGHT - self.rect.height
        if self.rect.y < 0:
            self.rect.y = 0

    def beveg(self, keys):
        vx, vy = 0, 0
        if keys[pg.K_LEFT]:
            vx = -self.speed
        if keys[pg.K_RIGHT]:
            vx = self.speed
        if keys[pg.K_UP]:
            vy = -self.speed
        if keys[pg.K_DOWN]:
            vy = self.speed
        self.rect.move_ip(vx, vy)
        self.plassering()

    def bærSau(self, sauer):
        for sau in sauer:
            if self.rect.colliderect(sau.rect) and self.color == RED:
                self.color = GREEN  # Endre fargen til grønn
                sauer.remove(sau)
                self.speed *= 0.9

    def sjekkKollisjon(self, spokelse, hindringer):
        global run
        if self.rect.colliderect(spokelse.rect):
            run = False
        for hindring in hindringer:
            if self.rect.colliderect(hindring.rect):
                self.rect.x -= 50
            if self.rect.colliderect(hindring.rect) and self.color == GREEN:
                self.rect.x += 70


class Sau(SpillObjekt):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)

class Hindring(SpillObjekt):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)

class Spokelse(SpillObjekt):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self.vx = 3
        self.vy = 3

    def beveg(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.x + self.rect.width >= 650 or self.rect.x <= 150:
            self.vx *= -1

        if self.rect.y + self.rect.height >= HEIGHT or self.rect.y <= 0:
            self.vy *= -1

# Lager et menneske objekt
menneske = Menneske(0, HEIGHT//2, 50, 50, RED, 4)

# Lager saue objekter
for i in range(3):
    while True:
        x = random.randint(700, 700)
        y = random.randint(0, 700)
        overlapping = any(s.rect.colliderect(pg.Rect(x, y, 50, 50)) for s in sauer)
        if not overlapping:
            sau = Sau(x, y, 50, 50, BLUE)
            sauer.append(sau)
            break

# Lager hindringsobjekter
for i in range(3):
    while True:
        hindring_x = random.randint(200, 600)
        hindring_y = random.randint(0, 800)
        overlapping = any(h.rect.colliderect(pg.Rect(hindring_x, hindring_y, 50, 50)) for h in hindringer)
        if not overlapping:
            hindring = Hindring(hindring_x, hindring_y, 50, 50, BLUE)
            hindringer.append(hindring)
            break

spokelse = Spokelse(WIDTH // 2, HEIGHT // 2, 50, 50, BLACK)

def poeng(menneske):
    poeng = 0
    if menneske.color == GREEN and menneske.rect.x <= 150:
        poeng += 1
    return poeng

while run:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    keys = pg.key.get_pressed()

    # Lager spillbrettet
    surface.fill(WHITE)
    pg.draw.rect(surface, LIGHTBLUE, pg.Rect(0, 0, 150, 800))
    pg.draw.rect(surface, LIGHTBLUE, pg.Rect(650, 0, 150, 800))

    menneske.beveg(keys)
    menneske.sjekkKollisjon(spokelse, hindringer)
    menneske.bærSau(sauer)
    menneske.tegn(surface)

    for sau in sauer:
        sau.tegn(surface)

    for hindring in hindringer:
        hindring.tegn(surface)

    # Beveg spøkelse
    spokelse.beveg()
    spokelse.tegn(surface)

    pg.display.flip()
    
pg.quit()
sys.exit()

print(f'Du har {poeng()} poeng!')
