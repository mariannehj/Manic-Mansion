#Importerer de nødvendige bibliotekene
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

#Lager tomme lister så jeg enkelt kan redigere antall sauer og hindringer på skjermen
sauer = []
hindringer = []

# Initiere pygame
pg.init()

# Lager en overflate (surface) jeg kan tegne på og tittel
surface = pg.display.set_mode(SIZE)
pg.display.set_caption("Manic Mansion")

#Lager en klokke
clock = pg.time.Clock()

#Variabel som styrer om spillet skal kjøres
run = True

#lager en superklasse spillobjekt, med det som skal være felles for alle objektene
class SpillObjekt:
    def __init__(self, x, y, width, height, color):
        self.rect = pg.Rect(x, y, width, height)
        self.color = color
        
#tegner objektene på surfacen
    def tegn(self, surface):
        pg.draw.rect(surface, self.color, self.rect)

#Lager en Menneskeklasse som arver fra SpillObjekt. Subklassen får en egen attributt speed
class Menneske(SpillObjekt):
    def __init__(self, x, y, width, height, color, speed: int):
        super().__init__(x, y, width, height, color)
        self.speed = speed

    #Plasserer mennesket på brettet. Objektet får en startposisjon, og det passes på at objektet ikke går utenfor rammen.
    def plassering(self):
        if self.rect.x + self.rect.width > WIDTH:
            self.rect.x = WIDTH - self.rect.width
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y + self.rect.height > HEIGHT:
            self.rect.y = HEIGHT - self.rect.height
        if self.rect.y < 0:
            self.rect.y = 0
            
    #Lager en metode slikat det er mulig å flytte på objektet, ved bruk av piltastene på tastaturet.
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

    #Lager en metode som plukker opp sauen, og da skifter farge og fart på mennesket objeket: Sauen forsvinner når den plukkes opp. Målet var å kunne legge fra seg sauen igjen, men det fikk jeg ikke til.
    def bærSau(self, sauer):
        for sau in sauer:
            if self.rect.colliderect(sau.rect) and self.color == RED:
                self.color = GREEN  # Endre fargen til grønn
                sauer.remove(sau)
                self.speed *= 0.9

    #Sjekker om mennesket kolliderer med spøkelset eller hindringene. Dersom det kolliderer med spøkelse, avsluttes spillet og brukeren har tapt. Dersom mennesket kolliderer med hindringene blir den kastet bakover.
    def sjekkKollisjon(self, spokelse, hindringer):
        global run
        if self.rect.colliderect(spokelse.rect):
            run = False
        for hindring in hindringer:
            if self.rect.colliderect(hindring.rect):
                self.rect.x -= 50
            if self.rect.colliderect(hindring.rect) and self.color == GREEN:
                self.rect.x += 70

#Sau og Hindring klassen har ingen egne attributter eller metoder

class Sau(SpillObjekt):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)

class Hindring(SpillObjekt):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)

#Spøkelse arver fra Superklasse, men har en egen fart vx, vy.
class Spokelse(SpillObjekt):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self.vx = 3
        self.vy = 3

    #Spøkelse beveger seg tilfelig med konstant fart
    def beveg(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        #Disse if-testene passer på at Spøkelse ikke beveger seg inn på friområdene.
        if self.rect.x + self.rect.width >= 650 or self.rect.x <= 150:
            self.vx *= -1

        if self.rect.y + self.rect.height >= HEIGHT or self.rect.y <= 0:
            self.vy *= -1

#Her skulle det gjerne vært en funksjon som lagde de ulike objektene, men det fikk jeg ikke til.
# Lager et menneske objekt
menneske = Menneske(0, HEIGHT//2, 50, 50, RED, 4)

#Når saue og hindringsobjektene lages, passes det på at de ikke overlapper med hverandre, som var et krav for oppgaven
# Lager saue-objekter
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
#Lager et spøkelses-jekt
spokelse = Spokelse(WIDTH // 2, HEIGHT // 2, 50, 50, BLACK)

""" 
Prøver her å telle poeng
def score(menneske):
    poeng = 0
    if menneske.color == GREEN and menneske.rect.x <= 150:
        poeng += 1
    return poeng

    her skal det også legges til flere hindringer og spøkelser
"""    

while run:
    #passer på hvor fort spillet kjører hver gang løkken går
    clock.tick(FPS)

    #Avslutter spillet hvis knappen for å lukke vinduet trykkes på.
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    #henter de ulike knappene som skal tryppes på
    keys = pg.key.get_pressed()

    # Lager spillbrettet
    surface.fill(WHITE)
    pg.draw.rect(surface, LIGHTBLUE, pg.Rect(0, 0, 150, 800))
    pg.draw.rect(surface, LIGHTBLUE, pg.Rect(650, 0, 150, 800))

    #Bruker metodene til menneske-objektet
    menneske.beveg(keys)
    menneske.sjekkKollisjon(spokelse, hindringer)
    menneske.bærSau(sauer)
    menneske.tegn(surface)

    #Tegner tre sauer, hvor alle har hver sin posisjon ved at jeg går gjennom listen og legger objektene til surfacen
    for sau in sauer:
        sau.tegn(surface)

    #Samme som for å legge til sauer
    for hindring in hindringer:
        hindring.tegn(surface)

    # Spøkelse blir lagt til spillbrettet og beveger seg.
    spokelse.beveg()
    spokelse.tegn(surface)

    #Flipper displayet helt til slutt så jeg er sikker på at alt vises.
    pg.display.flip()

#Avslutter pygame
pg.quit()
sys.exit()

#print(f'Du har {poeng()} poeng!')
