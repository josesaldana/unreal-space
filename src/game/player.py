import pygame
from pygame.sprite import Sprite, Group, spritecollide, spritecollideany
from pygame.mixer import Sound
from .missile import Missile
from .animations import PlayerHitAnimation

class Player(Sprite):
    def __init__(self, position = [0,0], score = 0, lifes = 100):
        Sprite.__init__(self)
        self.position = position
        self.image = pygame.image.load("assets/images/player.png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(topleft = self.position)
        self.score = score
        self.lifes = lifes
        self.missile = None
        self.hit_sound = Sound("assets/sound/187535-crash.ogg")

    def update(self):
        self.rect.x, self.rect.y = self.position

        if self.missile != None:
            self.missile.update()

    def shot(self, screen):
        self.missile = Missile(self.position)
        self.missile.emit_shot_sound()
        return self.missile

    def hit(self):
        self.hit_sound.play()
        return PlayerHitAnimation(self)