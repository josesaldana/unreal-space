import pygame

from pygame import draw, Color

class UIComponent(object):
    def __init__(self, size, pos):
        self.x, self.y = pos
        self.width, self.height = size

class LabelableUIComponent(UIComponent):
    def __init__(self, label, size, pos, font, label_color = Color("black")):
        super(LabelableUIComponent, self).__init__(size, pos)
        self.label = label
        self.font = font
        self.text_color = label_color
        self.image = self.font.render(self.label, True, self.text_color)
        self.rect = self.image.get_rect(center = (self.x + (self.width / 2), self.y + (self.height / 2)))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Text(LabelableUIComponent):
    def __init__(self, size, pos, text, font, color):
        super(Text, self).__init__(text, size, pos, font, color)

    def draw(self, surface):
        super(Text, self).draw(surface)

class Button2(LabelableUIComponent):
    def __init__(self, text, size, pos, font, color, active = False):
        super(Button2, self).__init__(text, size, pos, font, color)
        self.active = active
        self.background_color = Color("white") if self.active else Color("black")
        self.border = 5

    def draw(self, surface):
        pygame.draw.rect(surface, Color("white"), [self.x, self.y, self.width, self.height])
        pygame.draw.rect(surface, self.background_color, [self.x + self.border, self.y + self.border, self.width - 10, self.height - 10])

        super(Button2, self).draw(surface)

class Button:
    def __init__(self, text, siznpos, font = None, active = False):
        self.text = text
        self.active = active
        self.x, self.y, self.width, self.height = siznpos

        self.font = font if font is not None else pygame.font.Font(None, 26)
        self.text_color = Color("black") if self.active else Color("white")
        self.image = self.font.render(text, True, self.text_color)
        self.rect = self.image.get_rect(center = (self.x + (self.width / 2), self.y + (self.height / 2)))

        self.background_color = Color("white") if self.active else Color("black")
        self.border = 5

    def draw(self, surface):
        pygame.draw.rect(surface, Color("white"), [self.x, self.y, self.width, self.height])
        pygame.draw.rect(surface, self.background_color, [self.x + self.border, self.y + self.border, self.width - 10, self.height - 10])

        surface.blit(self.image, self.rect)

class Menu:
    def __init__(self, buttons):
        self.buttons = buttons
        self.selected_option = 0 if len(buttons) > 0 else -1

    def add_button(self, button):
        self.buttons.add(button)

    def select_option(self, direction):
        if direction > 0: self.selected_option += 1
        else: self.selected_option -= 1
        for btn in self.buttons: btn.active = False

        self.buttons[self.selected_option].active = True

    def draw(self, surface):
        for btn in self.buttons: btn.draw(surface)

    def update(self): pass
