"""
Main Menu Scene
"""

import pygame
from src.scenes.base_scene import Scene
from src.config import *


class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)

        self.menu_items = [
            "Start Race",
            "Customize Kart",
            "Select Track",
            "Quit"
        ]
        self.selected_item = 0

        # Menu colors
        self.title_color = YELLOW
        self.selected_color = ORANGE
        self.normal_color = WHITE

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_item = (
                    self.selected_item - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_item = (
                    self.selected_item + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.select_item()

    def select_item(self):
        """Handle menu item selection."""
        item = self.menu_items[self.selected_item]

        if item == "Start Race":
            self.game.change_state(PLAYING)
        elif item == "Customize Kart":
            self.game.change_state(CUSTOMIZATION)
        elif item == "Select Track":
            self.game.change_state(TRACK_SELECT)
        elif item == "Quit":
            self.game.quit_game()

    def update(self, dt):
        pass

    def draw(self, screen):
        # Draw title
        title_text = self.font_large.render(
            "KART RACING", True, self.title_color)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_text, title_rect)

        # Draw subtitle
        subtitle_text = self.font_small.render(
            "Race against AI opponents!", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(subtitle_text, subtitle_rect)

        # Draw menu items
        start_y = 300
        for i, item in enumerate(self.menu_items):
            color = self.selected_color if i == self.selected_item else self.normal_color
            text = self.font_medium.render(item, True, color)
            text_rect = text.get_rect(
                center=(SCREEN_WIDTH // 2, start_y + i * 60))
            screen.blit(text, text_rect)

        # Draw controls hint
        controls_text = self.font_small.render(
            "Use UP/DOWN arrows and ENTER to navigate", True, GRAY)
        controls_rect = controls_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(controls_text, controls_rect)
