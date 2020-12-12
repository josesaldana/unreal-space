import random, pygame
from random import randint
from pygame import draw, Color
from pygame.sprite import Sprite
from util import SpriteSheet
from game import GameConfig

class Asteroid(Sprite):
    def __init__(self, image_url, image_width, image_height, inset = None):
        super(Asteroid, self).__init__()
        self.sheet = SpriteSheet(image_url)
        self.images = self.sheet.images_by(image_width, image_height, Color("black"), inset)
        self.current_frame  = 0
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect(
            top = randint(-100, 0),
            left = randint(0, GameConfig.SCREEN_SIZE[0]),
            width = image_width,
            height = image_height
        )
        self.frame_speed = 1.5
        self.animation_counter = 0

    def update(self):
        if self.animation_counter == (self.frame_speed - 1):
            self.current_frame = (
                (self.current_frame + 1) if self.current_frame < len(self.images) else 0
            )
        self.animation_counter = (self.animation_counter + 1) % self.frame_speed
        self.image = self.images[self.current_frame - 1]

        if self.rect.y > GameConfig.SCREEN_SIZE[1]:
            self.rect.y = 0
            self.rect.x = random.randint(0, GameConfig.SCREEN_SIZE[0])
        else:
            self.rect.y += self.speed

class Asteroid100Points(Asteroid):
    def __init__(self):
        super(Asteroid100Points, self).__init__(
            "assets/images/100asteroid.png", 64, 64, (15, 15, 30, 30)
        )
        self.points = 100
        self.speed = 1

    def update(self):
        self.speed = randint(1, 5)
        super(Asteroid100Points, self).update()

class Asteroid500Points(Asteroid):
    def __init__(self):
        super(Asteroid500Points, self).__init__(
            "assets/images/200asteroid.png", 240, 320, (40, 84, 80, 150)
        )
        self.speed = 3
        self.points = 600

    def update(self):
        self.speed = randint(3, 5)
        super(Asteroid500Points, self).update()