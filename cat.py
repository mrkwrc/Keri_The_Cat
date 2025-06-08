import pygame
from pygame.sprite import Sprite
class Cat(Sprite):
    """A class to manage the cat."""
    
    def __init__(self, ai_game, image_scale=1.0):
        """Initialize the cat and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the Cat image and get its rect.
        # -------------------------------------------------------------------
        # Cat pixel art by Ei.
        # Source: https://opengameart.org/content/pixel-cat-and-courgette
        # license: CC0 / public domain
        # -------------------------------------------------------------------        
        image = pygame.image.load('images/cat.bmp')

        if image_scale != 1.0:
            width = int(image.get_width() * image_scale)
            height = int(image.get_height() * image_scale)
            self.image = pygame.transform.scale(image, (width, height))
        else:
            self.image = image

        self.rect = self.image.get_rect()

        # Start each new cat at the bottom center of the screen.
        self.rect.midleft = self.screen_rect.midleft

        # Store a decimal value for the cat's horizontal position.
        self.y = float(self.rect.y)

        # show the cat's movement
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the cat's position based on the movement flag."""
        # Update the cat's x value, not the rect.
        if self.moving_up and self.rect.top > 55:
            self.y -= self.settings.cat_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
           self.y += self.settings.cat_speed
        
        # Update the rect object from self.y.
        self.rect.y = self.y

    def blitme(self):
        """Draw the cat at its current location."""
        self.screen.blit(self.image, self.rect)


    def center_cat(self):
        """Center the cat on the screen."""
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)