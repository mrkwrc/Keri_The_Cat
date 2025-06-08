#!/usr/bin/env python3

import sys
from time import sleep
from random import random

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard

from button import Button
from cat import Cat
from heart import Heart
from pigeon import Pigeon

class CatGame:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self._screen_mode()
        pygame.display.set_caption("Keri The Cat")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.cat = Cat(self)
        self.hearts = pygame.sprite.Group()
        self.pigeons = pygame.sprite.Group()
        self.pigeons_hits = 0
        self.cat_hits = 0
        
        # Set the background color.
        self.bg_color = self.settings.bg_color
        
        # run the game in an active state.
        self.game_active = False

        # Create the Play button.
        self.play_button = Button(self, "P L A Y")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.game_active:
                self._create_pigeon()
                self.cat.update()
                # Get rid of hearts that have disappeared.
                self._update_hearts()
                self._update_pigeons()
            self._update_screen()
            self.clock.tick(60)
                
    def _screen_mode(self):
        """Set the screen mode based on user input."""
        if self.settings.fullscreen:
            # Set the screen to full screen mode.
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            # Set the screen to windowed mode.
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width,
                self.settings.screen_height)
            )
                
    def _check_events(self):
        """wait for the user to click keyboard or mouse"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._check_high_score_before_save()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self._start_game()

    def _start_game(self):
        """Start a new game if the Play button is clicked."""
        # Reset the game settings.
        self.settings.initialize_dynamic_settings()
        # Reset the game statistics.
        self.stats.reset_stats()
        self.sb.prep_stats_images()
        self.game_active = True
        # Empty the list of pigeons and bullets.
        self.pigeons.empty()
        self.hearts.empty()

        # Create a new pigeon and center the cat.
        self._create_pigeon()
        self.cat.center_cat()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False) 

    def _check_keyup_events(self, event):
        if event.key == pygame.K_UP:
                    # Stop moving the cat.
            self.cat.moving_up = False
        elif event.key == pygame.K_DOWN:
                    # Stop moving the cat.
            self.cat.moving_down = False

    def _check_keydown_events(self, event):
        if event.key == pygame.K_UP:
                    # Move the cat to the right.
            self.cat.moving_up = True
        elif event.key == pygame.K_DOWN:
                    # Move the cat to the left.
            self.cat.moving_down = True
        elif event.key == pygame.K_q:
            self._check_high_score_before_save()
            # Quit the game.
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_heart()
        elif event.key == pygame.K_g:
            # Start a new game by clicking the "g" key.
            self._start_game()
            
    def _fire_heart(self):
        """Create a new heart and add it to the hearts group."""
        if len(self.hearts) < self.settings.hearts_allowed:
            # Create a new heart and add it to the hearts group.
            new_heart = Heart(self)
            self.hearts.add(new_heart)

    def _update_hearts(self):
        """Update position of hearts and get rid of old hearts."""
        # Update heart positions.
        self.hearts.update()
        # Get rid of hearts that have disappeared.
        for heart in self.hearts.copy():
            if heart.rect.left >= self.settings.screen_width:
                self.hearts.remove(heart)
 
        # Check for any bullets that have hit a pigeon.
        # If so, get rid of the bullet and the pigeon.
        self._check_heart_pigeon_collisions()

    def _check_heart_pigeon_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.hearts, self.pigeons, False, False # base: True, True
        )       

        # Iterate through the collisions dictionary.
        for heart, pigeons_hit in collisions.items():
            # right edge of the heart
            heart_edge_x = heart.rect.right - (heart.rect.width / 2)

            for pigeon in pigeons_hit:
                pigeon_center_x = pigeon.rect.centerx
                pigeon_half_width = pigeon.rect.width / 2

                # Check if the heart's right edge 
                # is within the bounds of the pigeon.
                pigeon_left_bound = pigeon_center_x - (pigeon_half_width / 2)
                pigeon_right_bound = pigeon_center_x + (pigeon_half_width / 2)

                if pigeon_left_bound <= heart_edge_x <= pigeon_right_bound:
                    self.hearts.remove(heart)
                    self.pigeons.remove(pigeon)
                    self.settings.pigeon_hits += 1
                    self.stats.score += self.settings.pigeon_points
                    self.sb.prep_score()
                    self.sb.check_high_score()
                    self._start_next_level()
                    break 

    def _start_next_level(self):
        if self.settings.pigeon_hits >= self.settings.pigeon_hits_limit:
            # Increase the speed of the game.
            self.settings.increase_speed()
            # Update the scoreboard.
            self.stats.level += 1
            if self.stats.level % 5 == 0:
                self.settings.hearts_allowed += 1
            self.sb.prep_level()
            self.settings.pigeon_hits = 0    
                    
    def _update_pigeons(self):
        """Check if the fleet is at an edge,
        and update the positions of the pigeons.
        """
        # self._check_fleet_edges()
        self.pigeons.update()

        # Look for pigeon-cat collisions.
        if pygame.sprite.spritecollideany(self.cat, self.pigeons):
            self._cat_hit()
        
        # Look for pigeons that have hit the left side of the screen.
        self._check_pigeons_left()        

    def _create_pigeon(self):
        """Create pigeon, if conditions are right."""
        if random() < self.settings.pigeon_frequency:
            pigeon = Pigeon(self)
            self.pigeons.add(pigeon)

    def _update_screen(self):
        """refresh the screen during each pass through the loop"""
        self.screen.fill(self.settings.bg_color)
        self.pigeons.draw(self.screen)
        for heart in self.hearts.sprites():
            heart.draw_heart()        
        self.cat.blitme()

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()

        # present last modyfied screen
        pygame.display.flip()

    def _cat_hit(self):
        """Respond to the cat being hit by a pigeon."""
        if self.stats.cats_left > 0:
            # Decrement cats_left.
            self.stats.cats_left -= 1
            self.sb.prep_cats()

            # empty the list of pigeons and bullets.
            self.pigeons.empty()
            self.hearts.empty()

            # Create a new fleet and center the cat.
            #self._create_create()
            self.cat.center_cat()

            # Pause.
            sleep(0.5)
        else:
            self._check_high_score_before_save()
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_high_score_before_save(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
        self.stats.save_high_score_to_file()
    
    def _check_pigeons_left(self):
        """Check if any pigeons have reached the bottom of the screen."""
        for pigeon in self.pigeons.sprites():
            if pigeon.rect.left <= 0:
                # Treat this as a cat hit.
                self._cat_hit()
                break

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = CatGame()
    ai.run_game()