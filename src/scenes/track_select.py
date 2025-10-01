"""
Track Selection Scene
"""

import pygame
from src.scenes.base_scene import Scene
from src.config import *


class TrackSelectScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font_large = pygame.font.Font(None, 56)
        self.font_medium = pygame.font.Font(None, 42)
        self.font_small = pygame.font.Font(None, 32)

        self.tracks = [
            {"name": "Oval Circuit", "description": "Simple oval track for beginners"},
            {"name": "Forest Loop", "description": "Winding track through the forest"},
            {"name": "Desert Challenge", "description": "Sandy track with water hazards"}
        ]

        self.selected_track = self.game.selected_track

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_track = (
                    self.selected_track - 1) % len(self.tracks)
            elif event.key == pygame.K_RIGHT:
                self.selected_track = (
                    self.selected_track + 1) % len(self.tracks)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.game.selected_track = self.selected_track
                self.game.change_state(MENU)
            elif event.key == pygame.K_ESCAPE:
                self.game.change_state(MENU)

    def update(self, dt):
        pass

    def draw(self, screen):
        # Draw title
        title_text = self.font_large.render("SELECT TRACK", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_text, title_rect)

        # Draw track info
        track = self.tracks[self.selected_track]

        # Track name
        name_text = self.font_medium.render(track["name"], True, ORANGE)
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
        screen.blit(name_text, name_rect)

        # Track description
        desc_text = self.font_small.render(track["description"], True, WHITE)
        desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        screen.blit(desc_text, desc_rect)

        # Track preview (simple representation)
        preview_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 350, 200, 150)
        pygame.draw.rect(screen, DARK_GRAY, preview_rect)
        pygame.draw.rect(screen, WHITE, preview_rect, 3)

        preview_text = self.font_small.render("Track Preview", True, WHITE)
        preview_text_rect = preview_text.get_rect(center=preview_rect.center)
        screen.blit(preview_text, preview_text_rect)

        # Navigation arrows
        if self.selected_track > 0:
            left_text = self.font_medium.render("< ", True, ORANGE)
            screen.blit(left_text, (SCREEN_WIDTH // 2 - 200, 250))

        if self.selected_track < len(self.tracks) - 1:
            right_text = self.font_medium.render(" >", True, ORANGE)
            screen.blit(right_text, (SCREEN_WIDTH // 2 + 180, 250))

        # Track counter
        counter_text = self.font_small.render(
            f"{self.selected_track + 1} / {len(self.tracks)}", True, GRAY)
        counter_rect = counter_text.get_rect(center=(SCREEN_WIDTH // 2, 550))
        screen.blit(counter_text, counter_rect)

        # Controls
        controls_text = self.font_small.render(
            "LEFT/RIGHT: Navigate | ENTER: Select | ESC: Back", True, GRAY)
        controls_rect = controls_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(controls_text, controls_rect)
