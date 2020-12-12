from engine import *
from ui import *
from .game_config import GameConfig

class Credits(GameState):
    def __init__(self):
        super(Credits, self).__init__()
        self.font = pygame.font.Font(GameConfig.SUB_TITLE_FONT[0], 34)
        self.title = self.font.render("CREDITS", True, (255, 255, 255))
        self.title_rect = self.title.get_rect(x=(GameConfig.SCREEN_SIZE[0] / 2) - 80, y=50)
        self.next_state = "SPLASH"
        self.menu = Menu([
            Button("Back", ((GameConfig.SCREEN_SIZE[0] / 2) - 125, 390, 250, 40), active = True)
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

        center = GameConfig.SCREEN_SIZE[0] / 2

        Text((100, 20), (center - 50, 200), "Author",
            pygame.font.Font(GameConfig.SUB_TITLE_FONT[0], 18),
            Color("white")
        ).draw(surface)

        Text((100, 20), (center - 50, 230), "Jose Saldana",
            pygame.font.Font(None, 25),
            Color("white")
        ).draw(surface)

        Text((100, 20), (center - 50, 280), "Group",
            pygame.font.Font(GameConfig.SUB_TITLE_FONT[0], 18),
            Color("white")
        ).draw(surface)

        Text((100, 20), (center - 50, 310), "1LS-231",
            pygame.font.Font(None, 25),
            Color("white")
        ).draw(surface)