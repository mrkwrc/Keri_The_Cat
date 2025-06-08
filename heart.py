import pygame
from pygame.sprite import Sprite

class Heart(Sprite):
    """A class to manage hearts fired from the ship."""
    def __init__(self, ai_game):
        """Create a heart object at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.heart_color

        # Load the cat heart and get its rect.
        # -------------------------------------------------------------------
        # Heart pixel art by Flixberry Entertainment.
        # Source: https://opengameart.org/content/heart-pixel-art
        # license: CC-BY 4.0
        # -------------------------------------------------------------------
        self.image = pygame.image.load('images/hr.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midleft = ai_game.cat.rect.midleft

        # Store the heart's position as a decimal value.
        self.x = float(self.rect.x)

    def update(self):
        """Move the heart up the screen."""
        # Update the decimal position of the heart.
        self.x += self.settings.heart_speed
        # Update the rect position.
        self.rect.x = self.x

    def draw_heart(self):
        """Draw the heart to the screen."""
        self.screen.blit(self.image, self.rect)