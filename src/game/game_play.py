import pygame, random
from functools import reduce
from random import randrange, randint
from pygame.sprite import Sprite, Group, spritecollide, spritecollideany
from pygame.mixer import Sound
from engine import GameState
from .game_config import GameConfig
from .player import *
from .animations import *
from .asteroid import *
from .missile import *

class Gameplay(GameState):
    def __init__(self, screen):
        super(Gameplay, self).__init__()

        self.screen = screen

        self.game_over = False
        self.game_paused = False
        self.level_completed = False

        self.player = Player(GameConfig.INITIAL_POSITION)
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
            missile = self.player.shot(self.screen)
            self.missiles.add(missile)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game_paused = False if self.game_paused == True else True

    def update(self, dt):
        if self.game_paused:
            return

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
        pygame.draw.rect(surface, Color("black"), [0, 0, GameConfig.SCREEN_SIZE[0], 50])

        # Blit Title
        title_font = pygame.font.Font(GameConfig.MAIN_TITLE_FONT[0], 28)
        title = title_font.render(GameConfig.GAME_TITLE, True, Color("white"))
        surface.blit(title, [(GameConfig.SCREEN_SIZE[0] / 2) - 100, 10])

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
        sub_title_font = pygame.font.Font(GameConfig.SUB_TITLE_FONT[0], 18)
        score = sub_title_font.render("Score: " + str(self.player.score), True, Color("white"))
        lifes = sub_title_font.render("Lifes: ", True, Color("white"))
        surface.blit(score, [20, 20])
        surface.blit(lifes, [GameConfig.SCREEN_SIZE[0] - 150, 20])
        life_img = pygame.image.load("assets/images/life.png").convert()
        for life in range(0, int(self.player.lifes / 25)):
            surface.blit(life_img, [(GameConfig.SCREEN_SIZE[0] - 80) + (life * 20), 25])

    def draw_game_over(self, surface):
        text_font = pygame.font.Font(GameConfig.SUB_TITLE_FONT[0], 70)
        game_over_text = text_font.render("GAME OVER", True, Color("red"))
        surface.blit(game_over_text, [(GameConfig.SCREEN_SIZE[0] / 2) - 160, (GameConfig.SCREEN_SIZE[1] / 2) - 30])

    def draw_level_complete(self, surface):
        text_font = pygame.font.Font(GameConfig.SUB_TITLE_FONT[0], 40)
        game_over_text = text_font.render("Level Completed", True, Color("white"))
        surface.blit(game_over_text, [(GameConfig.SCREEN_SIZE[0] / 2) - 150, (GameConfig.SCREEN_SIZE[1] / 2) - 20])

    def draw_game_paused(self, surface):
        text_font = pygame.font.Font(GameConfig.SUB_TITLE_FONT[0], 40)
        game_over_text = text_font.render("Paused", True, Color("white"))
        surface.blit(game_over_text, [(GameConfig.SCREEN_SIZE[0] / 2) - 100, (GameConfig.SCREEN_SIZE[1] / 2) - 20])