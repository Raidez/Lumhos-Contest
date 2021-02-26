import arcade
import math
import random

WIDTH, HEIGHT = 600, 600
TITLE = "Lucioles"


def fade_color(start: arcade.Color, end: arcade.Color, factor: float) -> arcade.Color:
    factor = 0 if factor < 0 else 1 if factor > 1 else factor
    red = int(round(start[0] + (end[0] - start[0]) * factor))
    green = int(round(start[1] + (end[1] - start[1]) * factor))
    blue = int(round(start[2] + (end[2] - start[2]) * factor))
    blend = (red, green, blue)
    return blend


class Firefly(arcade.SpriteCircle):
    WIDTH, HEIGHT = 0, 0
    SPEED = (10, 50)
    LIGHTUP_TIME = 1
    BRIGHT = (173, 255, 0)
    DARKER = (26, 36, 7)
    FADE_SOUND = 0.8
    SOUND = "assets/sound/fireflies_shaked.ogg"

    def __init__(
        self, x, y, r=5, *, speed: int, target: arcade.Point, timer=0, countdown: float
    ):
        super().__init__(r, self.BRIGHT)
        self.center_x = x
        self.center_y = y
        self.target = target
        self.timer = timer
        self.original_speed = speed
        self.speed = speed
        self.countdown = countdown
        self.is_shaked = False

    def on_update(self, delta: float):
        if self.is_shaked:
            # la luciole est agitée par le clique
            self.color = self.BRIGHT
        else:
            # gestion du timer pour changer la couleur
            self.timer += delta
            if self.timer > self.countdown:
                self.timer -= self.countdown

            # changement de la couleur
            step = self.timer / self.LIGHTUP_TIME
            self.color = fade_color(self.BRIGHT, self.DARKER, step)

        # calcul de la nouvelle position pour atteindre la cible
        angle = math.atan2(self.target.y - self.center_y, self.target.x - self.center_x)
        self.change_x = self.speed * delta * math.cos(angle)
        self.change_y = self.speed * delta * math.sin(angle)

        # vérification si on a atteint la cible
        if self.collides_with_point(self.target):
            self.target = self.find_new_target()

        super().update()

    @classmethod
    def find_new_target(cls):
        return arcade.NamedPoint(
            random.randint(0, cls.WIDTH), random.randint(0, cls.HEIGHT)
        )


class Mouse(arcade.SpriteCircle):
    COLOR = (236, 100, 75)

    def __init__(self):
        super().__init__(50, self.COLOR)
        self.radius = 50
        self.display = False
        self.firefly_sound = None
        self.player_sound = None
        self.fade = 0

    def update(self, delta, fireflies, shaked_fireflies: set):
        firefly_shaked = lambda mouse: arcade.NamedPoint(
            random.uniform(
                mouse.center_x - mouse.radius, mouse.center_x + mouse.radius
            ),
            random.uniform(
                mouse.center_y - mouse.radius, mouse.center_y + mouse.radius
            ),
        )

        if self.display:
            # si l'utilisateur clique, les lucioles sont attirées
            for f in fireflies:
                if f.collides_with_sprite(self):  ## collision avec la souris
                    f.is_shaked = True
                    f.target = firefly_shaked(self)
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
        volume = lambda: self.fade / Firefly.FADE_SOUND
        if len(shaked_fireflies):
            ## création du son / fade in
            self.fade = min(1, self.fade + delta)
            if not self.player_sound:
                self.player_sound = arcade.play_sound(
                    self.firefly_sound, volume=volume(), looping=True
                )
            else:
                self.firefly_sound.set_volume(volume(), self.player_sound)
        elif not len(shaked_fireflies) and self.player_sound:
            ## supression du son / fade out
            self.fade = max(0, self.fade - delta)
            if volume() > 0:
                self.firefly_sound.set_volume(volume(), self.player_sound)
            else:
                arcade.stop_sound(self.player_sound)
                self.player_sound = None

    def draw(self):
        if self.display:
            super().draw()


class FadingMessage(arcade.Sprite):
    COLOR_START = None
    COLOR_END = arcade.csscolor.LIGHT_PINK
    FONT_NAME = "segoesc"
    FONT_SIZE = 32
    FADE_TIMER = 2
    FADE_IN = 2
    FADE_OUT = 0.8
    COUNTDOWN = 3

    def __init__(self, x, y, text):
        super().__init__(center_x=x, center_y=y)
        self.y = y
        self.text = text
        self.color = self.COLOR_START
        self.start_color = self.COLOR_START
        self.timer = 0.0
        self.countdown = 0.0
        self.status = "fade in"
        self.speed = 50

    def on_update(self, delta: float):
        self.countdown += delta

        # le message apparait
        if self.status == "fade in" and self.countdown > self.COUNTDOWN:
            if self.center_y > self.y - 50:
                self.center_y -= self.speed * delta

            self.timer = min(1, self.timer + delta / self.FADE_IN)
            self.color = fade_color(self.COLOR_START, self.COLOR_END, self.timer)
        # le message disparait
        elif self.status == "fade out":
            if self.center_y > self.y - 100:
                self.center_y -= self.speed * delta

            self.timer = max(0, self.timer - delta / self.FADE_OUT)
            self.color = fade_color(self.COLOR_START, self.start_color, self.timer)

        super().update()

    def draw(self):
        arcade.draw_text(
            self.text,
            self.center_x,
            self.center_y,
            color=self.color,
            font_name=self.FONT_NAME,
            font_size=self.FONT_SIZE,
            align="center",
            anchor_x="center",
            anchor_y="center",
        )


class MyGame(arcade.Window):
    BACKGROUND = arcade.csscolor.BLACK
    MUSIC = "assets/music/fireflies.ogg"

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        Firefly.WIDTH, Firefly.HEIGHT = width, height
        arcade.set_background_color(self.BACKGROUND)

        self.message = None
        self.fireflies = None
        self.shaked_fireflies = None
        self.mouse = None
        self.music = arcade.load_sound(self.MUSIC, streaming=True)
        self.firefly_sound = arcade.load_sound(Firefly.SOUND)

    def setup(self, nb: int = 100):
        # préchargement du son (sinon freeze)
        arcade.stop_sound(arcade.play_sound(self.firefly_sound))

        # lancement de la musique
        arcade.play_sound(self.music, volume=0.5, looping=True)

        # objet conteneur de la souris
        self.mouse = Mouse()
        self.mouse.firefly_sound = self.firefly_sound

        # message
        FadingMessage.COLOR_START = self.BACKGROUND
        self.message = FadingMessage(
            self.width / 2, self.height, "clique avec la souris"
        )

        # initialisation des lucioles aléatoirement (position, taille, cible, état de l'éclairage, vitesse d'éclairage)
        self.shaked_fireflies = set()
        self.fireflies = arcade.SpriteList()
        for _ in range(nb):
            x, y, r = (
                random.randint(0, self.width),
                random.randint(0, self.height),
                random.randint(4, 7),
            )
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
            self.fireflies.append(f)

    def on_update(self, delta: float):
        self.message.on_update(delta)
        self.mouse.update(delta, self.fireflies, self.shaked_fireflies)
        self.fireflies.on_update(delta)

    def on_draw(self):
        arcade.start_render()
        self.message.draw()
        self.mouse.draw()
        self.fireflies.draw()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # mise à jour de la position de la souris
        self.mouse.center_x = x
        self.mouse.center_y = y

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.mouse.display = False

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.mouse.display = True

        # click alors que le message n'as pas fini de descendre
        if button == arcade.MOUSE_BUTTON_LEFT and self.message.status == "fade in":
            self.message.start_color = self.message.color
            self.message.status = "fade out"
            self.message.timer = 1


if __name__ == "__main__":
    game = MyGame(WIDTH, HEIGHT, TITLE)
    game.setup()
    arcade.run()
