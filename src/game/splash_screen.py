import pygame
from pygame import Color
from pygame.mixer import Sound
from engine import GameState
from ui import Button, Menu
from engine import GameState
from .game_config import GameConfig

class SplashScreen(GameState):
    def __init__(self, SCREEN_SIZE = [800, 650]):
        super(SplashScreen, self).__init__()
        self.font = pygame.font.Font(GameConfig.MAIN_TITLE_FONT[0], 54)
        self.title = self.font.render(GameConfig.GAME_TITLE, True, (229, 22, 22))
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
        surface.blit(background, [(GameConfig.SCREEN_SIZE[0] / 2) - 250, (GameConfig.SCREEN_SIZE[1] / 2) - 140])
        surface.blit(self.title, self.title_rect)
        self.menu.draw(surface)

    def update(self, surface):
        self.menu.update()