from pygame.sprite import Sprite, Group, spritecollide, spritecollideany
from pygame.mixer import Sound
from util import SpriteSheet

class PlayerHitAnimation(Sprite):
    def __init__(self, player):
        super(PlayerHitAnimation, self).__init__()
        self.player = player
        self.sheet = SpriteSheet("assets/images/Sprite_FX_Explosion_0042.png")
        self.images = self.sheet.images_by(148, 148, (0, 0, 0))
        self.current_frame = 0
        self.frame_speed = 2
        self.animation_counter = 0
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect(
            left = self.player.rect.x, top = self.player.rect.y
        )

    def update(self):
        if self.animation_counter == (self.frame_speed - 1):
            self.current_frame = (self.current_frame + 1) % len(self.images)
        self.animation_counter = (self.animation_counter + 1) % self.frame_speed

        self.image = self.images[self.current_frame - 1]
        self.rect = self.image.get_rect(
            left = self.player.rect.x, top = self.player.rect.y
        )

        if self.current_frame == len(self.images) - 1:
            self.kill()

class AsteroidExplosion(Sprite):
    def __init__(self, exploded_object):
        super(AsteroidExplosion, self).__init__()
        self.exploded_object = exploded_object
        self.sheet = SpriteSheet("assets/images/Sprite_FX_Explosion_0015.png")
        self.images = self.sheet.images_at(
            [
                (52, 88, 118, 124), (268, 72, 136, 140), (480, 70, 158, 160),
                (699, 62, 172, 168), (914, 82, 186, 186), (1140, 46, 200, 190),
                (1106, 558, 246, 328)
            ],
            (0, 128, 0)
        )
        self.current_frame  = 0
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect(top = exploded_object.y, left = exploded_object.x)
        self.sound = Sound("assets/sound/Explosion-SoundBible.com-2019248186.wav")

    def update(self):
        self.current_frame = (self.current_frame + 1) % len(self.images)
        self.image = self.images[self.current_frame - 1]
        self.rect = self.image.get_rect(
            topleft = (
                (self.exploded_object.x + self.exploded_object.width / 2) - (self.image.get_width() / 2),
                (self.exploded_object.y + self.exploded_object.height / 2) - (self.image.get_height() / 2)
            )
        )

        if self.current_frame == 0:
            self.kill()