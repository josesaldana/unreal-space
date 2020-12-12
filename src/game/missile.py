import pygame
from pygame.sprite import Sprite
from pygame.mixer import Sound

class Missile(Sprite):
    def __init__(self, ship_pos):
        super(Missile, self).__init__()
        self.image = pygame.Surface([2, 10])
        self.image.fill([255, 255, 255])
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = ship_pos[0] + 45
        self.rect.y = ship_pos[1] - 10
        self.sonido = Sound("assets/sound/laser4.wav")

    def update(self):
        self.rect.y -= 10

    def emit_shot_sound(self):
        self.sonido.play()