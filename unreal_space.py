import pygame
import sys
import random
import os
import pygame.transform
from random import randrange, randint
from engine import Game, GameState
from pygame import draw, Color
from pygame.sprite import Sprite, Group, spritecollide, spritecollideany
from ui import Text, Button, Menu
from util import SpriteSheet
from pygame.mixer import Sound

### Game Constants ###
SCREEN_SIZE = [800, 650]
INITIAL_POSITION = [(SCREEN_SIZE[0] / 2) - 100, SCREEN_SIZE[1] - 100]
DEFAULT_TEXT_FONT = (None, 26)
SUB_TITLE_FONT = ("assets/Fonts/Coda-Regular.ttf", 40)
MAIN_TITLE_FONT = ("assets/Fonts/BowlbyOne-Regular.ttf", 64)
GAME_TITLE = "Unreal Space"

### Game Objects ###
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

class Missile(Sprite):
    def __init__(self, ship_pos):
        super(Missile, self).__init__()
        self.image = pygame.Surface([2, 10])
        self.image.fill([255, 255, 255])
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = ship_pos[0] + 45
        self.rect.y = ship_pos[1] - 10
        self.sonido = pygame.mixer.Sound("assets/sound/laser4.wav")

    def update(self):
        self.rect.y -= 10

    def emit_shot_sound(self):
        self.sonido.play()

class Asteroid(Sprite):
    def __init__(self, image_url, image_width, image_height, inset = None):
        super(Asteroid, self).__init__()
        self.sheet = SpriteSheet(image_url)
        self.images = self.sheet.images_by(image_width, image_height, Color("black"), inset)
        self.current_frame  = 0
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect(
            top = randint(-100, 0),
            left = randint(0, SCREEN_SIZE[0]),
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

        if self.rect.y > SCREEN_SIZE[1]:
            self.rect.y = 0
            self.rect.x = random.randint(0, SCREEN_SIZE[0])
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

### Stages ####
class SplashScreen(GameState):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.font = pygame.font.Font(MAIN_TITLE_FONT[0], 54)
        self.title = self.font.render(GAME_TITLE, True, (229, 22, 22))
        self.title_rect = self.title.get_rect(x=(SCREEN_SIZE[0] / 2) - 220, y=80)
        self.persist["screen_color"] = "black"
        self.next_state = "GAMEPLAY"
        self.menu = Menu([
            Button("Start", ((SCREEN_SIZE[0] / 2) - 125, 300, 250, 40)),
            Button("Credits", ((SCREEN_SIZE[0] / 2) - 125, 350, 250, 40))
        ])
        self.sound = Sound("assets/sound/MainTheme.wav")
        self.sound.play()

    def startup(self, persistent):
        self.sound.play()
        self.menu.select_option(0)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.menu.select_option(-1)
            elif event.key == pygame.K_DOWN:
                self.menu.select_option(1)
            elif event.key == pygame.K_RETURN:
                self.next_state = "GAMEPLAY" if self.menu.selected_option == 0 else "CREDITS"
                self.persist["selected_option"] = self.menu.selected_option
                self.done = True
                self.sound.stop()

    def draw(self, surface):
        surface.fill(Color("black"))
        background = pygame.image.load("assets/images/nave.png").convert()
        background.set_colorkey((255, 255, 255))
        surface.blit(background, [(SCREEN_SIZE[0] / 2) - 250, (SCREEN_SIZE[1] / 2) - 140])
        surface.blit(self.title, self.title_rect)
        self.menu.draw(surface)

    def update(self, surface):
        self.menu.update()

class Credits(GameState):
    def __init__(self):
        super(Credits, self).__init__()
        self.font = pygame.font.Font(SUB_TITLE_FONT[0], 34)
        self.title = self.font.render("CREDITS", True, (255, 255, 255))
        self.title_rect = self.title.get_rect(x=(SCREEN_SIZE[0] / 2) - 80, y=50)
        self.next_state = "SPLASH"
        self.menu = Menu([
            Button("Back", ((SCREEN_SIZE[0] / 2) - 125, 390, 250, 40), active = True)
        ])

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            self.done = True

    def draw(self, surface):
        surface.fill(Color("black"))
        surface.blit(self.title, self.title_rect)
        self.menu.draw(surface)

        center = SCREEN_SIZE[0] / 2

        Text((100, 20), (center - 50, 200), "Author",
            pygame.font.Font(SUB_TITLE_FONT[0], 18),
            Color("white")
        ).draw(surface)

        Text((100, 20), (center - 50, 230), "Jose Saldana",
            pygame.font.Font(None, 25),
            Color("white")
        ).draw(surface)

        Text((100, 20), (center - 50, 280), "Group",
            pygame.font.Font(SUB_TITLE_FONT[0], 18),
            Color("white")
        ).draw(surface)

        Text((100, 20), (center - 50, 310), "1LS-231",
            pygame.font.Font(None, 25),
            Color("white")
        ).draw(surface)

class Gameplay(GameState):
    def __init__(self):
        super(Gameplay, self).__init__()

        self.game_over = False
        self.game_paused = False
        self.level_completed = False

        self.player = Player(INITIAL_POSITION)
        self.missiles = Group()

        self._100pts_asteroids = pygame.sprite.Group()
        self._500pts_asteroids = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.asteroids.add(self._100pts_asteroids)
        self.asteroids.add(self._500pts_asteroids)

        self.explosions_group = Group()
        self.player_hits_group = Group()

        self.sound = Sound("assets/sound/FranticLevel.wav")
        self.level_complete_sound = Sound("assets/sound/HappyLevel.wav")
        self.game_over_sound = Sound("assets/sound/oops.wav")

    def startup(self, persistent):
        self.persist = persistent
        color = self.persist["screen_color"]
        self.screen_color = pygame.Color(color)

        # 100 Points asteroids
        self._100pts_asteroids.add([Asteroid100Points() for i in range(0, randint(1, 40))])
        self.asteroids.add(self._100pts_asteroids)

        # 200 Points asteroids
        self._500pts_asteroids.add([Asteroid500Points() for i in range(0, randint(1, 10))])
        self.asteroids.add(self._500pts_asteroids)

        self.sound.play(loops = -1)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            missile = self.player.shot(screen)
            self.missiles.add(missile)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game_paused = False if self.game_paused == True else True

    def update(self, dt):
        if not self.game_paused:
            # Asteroid hit by missile
            for m in self.missiles.sprites():
                collided_asteroids = spritecollide(m, self.asteroids, True)

                for collided_asteroid in collided_asteroids:
                    if not self.game_over:
                        self.player.score += collided_asteroid.points

                    # Explosion
                    explosion = AsteroidExplosion(collided_asteroid.rect)
                    self.explosions_group.add(explosion)
                    explosion.sound.play()

                    # Remove both asteroid and missile
                    collided_asteroid.kill()
                    m.kill()

            if len(self.asteroids.sprites()) == 0:
                self.level_completed = True

            # Ship hit by asteroid
            collided_asteroids = spritecollide(self.player, self.asteroids, True)

            if len(collided_asteroids) > 0:
                self.player_hits_group.add(self.player.hit())

            if not self.game_over:
                collided_points = map((lambda a: a.points / 20), collided_asteroids)
                self.player.lifes -= reduce((lambda x, y: x + y), collided_points, 0)

            if self.player.lifes <= 0:
                self.game_over = True

            # Sprites and groups update
            self.player.update()
            self.asteroids.update()
            self.missiles.update()
            self.explosions_group.update()
            self.player_hits_group.update()

    def draw(self, surface):
        # Set background
        surface.fill(self.screen_color)
        background = pygame.image.load("assets/images/saturn.jpg").convert()
        surface.blit(background, [0, 0])

        # Draw player
        self.player.position = pygame.mouse.get_pos()
        surface.blit(self.player.image, self.player.rect)

        # Draw asteroids
        self.asteroids.draw(surface)
        self.missiles.draw(surface)
        self.explosions_group.draw(surface)
        self.player_hits_group.draw(surface)

        # Draw title bar
        pygame.draw.rect(surface, Color("black"), [0, 0, SCREEN_SIZE[0], 50])

        # Blit Title
        title_font = pygame.font.Font(MAIN_TITLE_FONT[0], 28)
        title = title_font.render(GAME_TITLE, True, Color("white"))
        surface.blit(title, [(SCREEN_SIZE[0] / 2) - 100, 10])

        # Draw the title bar
        self.draw_title_bar(surface)

        # Draw Game Paused
        if self.game_paused and not (self.level_completed or self.game_over):
            self.draw_game_paused(surface)

        # Draw Level Completed
        if self.level_completed and not self.game_over:
            self.draw_level_complete(surface)
            self.sound.stop()
            self.level_complete_sound.play()

        # Draw Game Over if applicable
        if self.game_over:
            self.draw_game_over(surface)
            self.sound.stop()
            self.game_over_sound.play()

    def draw_title_bar(self, surface):
        sub_title_font = pygame.font.Font(SUB_TITLE_FONT[0], 18)
        score = sub_title_font.render("Score: " + str(self.player.score), True, Color("white"))
        lifes = sub_title_font.render("Lifes: ", True, Color("white"))
        surface.blit(score, [20, 20])
        surface.blit(lifes, [SCREEN_SIZE[0] - 150, 20])
        life_img = pygame.image.load("assets/images/life.png").convert()
        for life in range(0, self.player.lifes / 25):
            surface.blit(life_img, [(SCREEN_SIZE[0] - 80) + (life * 20), 25])

    def draw_game_over(self, surface):
        text_font = pygame.font.Font(SUB_TITLE_FONT[0], 70)
        game_over_text = text_font.render("GAME OVER", True, Color("red"))
        surface.blit(game_over_text, [(SCREEN_SIZE[0] / 2) - 160, (SCREEN_SIZE[1] / 2) - 30])

    def draw_level_complete(self, surface):
        text_font = pygame.font.Font(SUB_TITLE_FONT[0], 40)
        game_over_text = text_font.render("Level Completed", True, Color("white"))
        surface.blit(game_over_text, [(SCREEN_SIZE[0] / 2) - 150, (SCREEN_SIZE[1] / 2) - 20])

    def draw_game_paused(self, surface):
        text_font = pygame.font.Font(SUB_TITLE_FONT[0], 40)
        game_over_text = text_font.render("Paused", True, Color("white"))
        surface.blit(game_over_text, [(SCREEN_SIZE[0] / 2) - 100, (SCREEN_SIZE[1] / 2) - 20])

### Main Entry Point ###
if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)

    pygame.mouse.set_visible(False)
    pygame.mouse.set_pos(INITIAL_POSITION)

    states = {
        "SPLASH": SplashScreen(),
        "GAMEPLAY": Gameplay(),
        "CREDITS": Credits()
    }

    game = Game(screen, states, "SPLASH")
    game.run()

    pygame.quit()
    sys.exit()
