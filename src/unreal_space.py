import sys
import pygame
from engine import Game
from game import GameConfig, SplashScreen, Gameplay, Credits

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode(GameConfig.SCREEN_SIZE)

    pygame.mouse.set_visible(False)
    pygame.mouse.set_pos(GameConfig.INITIAL_POSITION)

    states = {
        "SPLASH": SplashScreen(),
        "GAMEPLAY": Gameplay(screen),
        "CREDITS": Credits()
    }

    game = Game(screen, states, "SPLASH")
    game.run()

    pygame.quit()
    sys.exit()
