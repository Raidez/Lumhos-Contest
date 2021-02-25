import math
import pygame
import random

from pygame import Color
from pygame.locals import *

from shapes import Circ, Text, fade_color

# documentation: https://www.pygame.org/docs/index.html
# tutoriel: https://pythonturtle.academy/tutorial-fireflies/
# musique: https://youtu.be/nziK7zv8qDI

WIDTH, HEIGHT = 600, 600
TITLE = "Lucioles"
FPS = 60
BACKGROUND = Color("black")

#################################################################################

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# musique de fond
pygame.mixer.music.load("assets/music/fireflies.ogg")
pygame.mixer.music.play(-1)


class Firefly(Circ):
    SPEED = (10, 50)
    LIGHTUP_TIME = 1
    BRIGHT = Color(173, 255, 0)
    DARKER = Color(26, 36, 7)
    SOUND = pygame.mixer.Sound("assets/sound/fireflies_shaked.ogg")
    FADESOUND = 800

    def __init__(
        self, x, y, r=5, *, speed: int, target: Circ, timer=0, countdown: float
    ):
        super().__init__(x, y, r)
        self.color = Firefly.DARKER
        self.target = target
        self.timer = timer
        self.original_speed = speed
        self.speed = speed
        self.countdown = countdown
        self.is_shaked = False

    def update(self, delta: float) -> bool:
        if self.is_shaked:
            # la luciole est agitée par le clique
            self.color = Firefly.BRIGHT
        else:
            # gestion du timer pour changer la couleur
            self.timer += delta / 1000
            if self.timer > self.countdown:
                self.timer -= self.countdown

            # changement de la couleur
            step = self.timer / Firefly.LIGHTUP_TIME
            self.color = fade_color(Firefly.BRIGHT, Firefly.DARKER, step)

        # calcul de la nouvelle position pour atteindre la cible
        angle = math.atan2(self.target.y - self.y, self.target.x - self.x)
        self.x += self.speed * delta / 1000 * math.cos(angle)
        self.y += self.speed * delta / 1000 * math.sin(angle)

        # vérification si on a atteint la cible
        if self.collide(self.target):
            self.target = Firefly.find_new_target()

    def draw(self, surface: pygame.Surface):
        super().draw(surface, self.color)

    @staticmethod
    def find_new_target():
        return Circ(random.uniform(0, WIDTH), random.uniform(0, HEIGHT), 16)


class Mouse(Circ):
    COLOR = Color(236, 100, 75)

    def __init__(self):
        super().__init__(0, 0, 50)
        self.display = False

    def update(self, delta: float, fireflies, shaked_fireflies):
        firefly_shaked = lambda mouse: Circ(
            random.uniform(mouse.x - mouse.r, mouse.x + mouse.r),
            random.uniform(mouse.y - mouse.r, mouse.y + mouse.r),
        )

        left_click = pygame.mouse.get_pressed()[0]
        self.x, self.y = pygame.mouse.get_pos()
        self.display = left_click

        if left_click:
            # si l'utilisateur clique, les lucioles sont attirées
            for f in fireflies:
                if f.collide(mouse):  ## collision avec la souris
                    f.is_shaked = True
                    f.target = firefly_shaked(mouse)
                    f.speed = 100
                    shaked_fireflies.add(f)
                elif (
                    f in shaked_fireflies
                ):  ## elles ne sont plus dans la range de la souris
                    f.is_shaked = False
                    f.speed = f.original_speed
                    shaked_fireflies.remove(f)
        else:
            # les lucioles retournent à leur business
            for f in shaked_fireflies:
                f.is_shaked = False
                f.target = Firefly.find_new_target()
                f.speed = (
                    f.original_speed
                )  ## on rétablit la vitesse par défaut de la luciole
                f.timer = random.uniform(0.0, f.countdown)

            shaked_fireflies.clear()

        # gestion du son
        if len(shaked_fireflies):
            Firefly.SOUND.play(fade_ms=Firefly.FADESOUND)
        else:
            Firefly.SOUND.fadeout(Firefly.FADESOUND)

    def draw(self, surface: pygame.Surface):
        super().draw(surface, Mouse.COLOR)


class FadingMessage(Text):
    COLOR_START = BACKGROUND
    COLOR_END = Color(255, 182, 193)
    FONTNAME = "segoescript"
    FONTSIZE = 32
    FADETIMER = 2000
    FADEIN = 2000
    FADEOUT = 800
    COUNTDOWN = 3000

    def __init__(self, x, y, text):
        super().__init__(
            x,
            y,
            text,
            center=True,
            font=FadingMessage.FONTNAME,
            size=FadingMessage.FONTSIZE,
        )
        self.color = FadingMessage.COLOR_START
        self.timer = 0.0
        self.countdown = 0.0
        self.status = "fade in"
        self.speed = 50

    def update(self, delta: float):
        left_click = pygame.mouse.get_pressed()[0]
        self.countdown += delta

        # click alors que le message n'as pas fini de descendre
        if self.status == "fade in" and left_click:
            self.start_color = message.color
            self.status = "fade out"
            self.timer = 0

        # le message apparait
        if self.status == "fade in" and self.countdown > FadingMessage.COUNTDOWN:
            if self.y < 50:
                self.y += self.speed * delta / 1000
            self.timer += delta / FadingMessage.FADEIN
            self.color = fade_color(
                FadingMessage.COLOR_START, FadingMessage.COLOR_END, self.timer
            )
        # le message disparait
        elif self.status == "fade out":
            if self.y < 100:
                self.y += self.speed * delta / 1000
            self.timer += delta / FadingMessage.FADEOUT
            self.color = fade_color(
                self.start_color, FadingMessage.COLOR_START, self.timer
            )

    def draw(self, surface: pygame.Surface):
        super().draw(surface, self.color)


nb = 100  # nombre de lucioles
mouse = Mouse()  # objet conteneur de la souris
message = FadingMessage(WIDTH / 2, 0, "clique avec la souris")

# initialisation des lucioles aléatoirement (position, taille, cible, état de l'éclairage, vitesse d'éclairage)
fireflies = list()
shaked_fireflies = set()
for _ in range(nb):
    x, y, r = random.uniform(0, WIDTH), random.uniform(0, HEIGHT), random.uniform(4, 7)
    countdown = random.uniform(1, 5)
    timer = random.uniform(0, countdown)

    f = Firefly(
        x,
        y,
        r,
        speed=random.uniform(*Firefly.SPEED),
        timer=timer,
        target=Firefly.find_new_target(),
        countdown=countdown,
    )
    fireflies.append(f)

#################################################################################
running = True
while running:
    ### UPDATE ###
    delta = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # mise à jour de la position du message avec un timeout
    message.update(delta)

    # gestion de la souris pour attirer les lucioles
    mouse.update(delta, fireflies, shaked_fireflies)

    # mise à jour des lucioles (mouvement, couleur)
    for f in fireflies:
        f.update(delta)

    ### DRAW ###
    screen.fill(BACKGROUND)

    # si l'utilisateur n'as pas cliqué, on affiche un message
    message.draw(screen)

    # affiche de la souris
    if mouse.display:
        mouse.draw(screen)

    # affichage des lucioles
    for f in fireflies:
        f.draw(screen)

    pygame.display.update()

pygame.quit()
