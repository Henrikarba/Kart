"""
Kart Customization Scene
"""

import pygame
from src.scenes.base_scene import Scene
from src.config import *


class CustomizationScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font_large = pygame.font.Font(None, 56)
        self.font_medium = pygame.font.Font(None, 42)
        self.font_small = pygame.font.Font(None, 32)

        self.colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE]
        self.color_names = ["Red", "Blue",
                            "Green", "Yellow", "Purple", "Orange"]

        self.attributes = ["Color", "Max Speed", "Acceleration", "Turn Speed"]
        self.selected_attribute = 0

        # Current kart configuration
        self.kart_config = self.game.player_kart_config.copy()
        self.selected_color = self.colors.index(self.kart_config['color'])

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_attribute = (
                    self.selected_attribute - 1) % len(self.attributes)
            elif event.key == pygame.K_DOWN:
                self.selected_attribute = (
                    self.selected_attribute + 1) % len(self.attributes)
            elif event.key == pygame.K_LEFT:
                self.adjust_attribute(-1)
            elif event.key == pygame.K_RIGHT:
                self.adjust_attribute(1)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Save configuration and return to menu
                self.game.player_kart_config = self.kart_config.copy()
                self.game.change_state(MENU)
            elif event.key == pygame.K_ESCAPE:
                self.game.change_state(MENU)

    def adjust_attribute(self, direction):
        """Adjust the selected attribute."""
        attribute = self.attributes[self.selected_attribute]

        if attribute == "Color":
            self.selected_color = (
                self.selected_color + direction) % len(self.colors)
            self.kart_config['color'] = self.colors[self.selected_color]
        elif attribute == "Max Speed":
            self.kart_config['max_speed'] = max(
                4, min(12, self.kart_config['max_speed'] + direction * 0.5))
        elif attribute == "Acceleration":
            self.kart_config['acceleration'] = max(
                0.1, min(0.8, self.kart_config['acceleration'] + direction * 0.05))
        elif attribute == "Turn Speed":
            self.kart_config['turn_speed'] = max(
                2, min(8, self.kart_config['turn_speed'] + direction * 0.5))

    def update(self, dt):
        pass

    def draw(self, screen):
        # Draw title
        title_text = self.font_large.render("CUSTOMIZE KART", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(title_text, title_rect)

        # Draw kart preview
        kart_center = (SCREEN_WIDTH // 2 - 200, 250)
        pygame.draw.circle(screen, self.kart_config['color'], kart_center, 30)
        pygame.draw.circle(screen, BLACK, kart_center, 30, 3)

        # Draw attribute list
        start_y = 180
        for i, attribute in enumerate(self.attributes):
            color = ORANGE if i == self.selected_attribute else WHITE
            attr_text = self.font_medium.render(attribute + ":", True, color)
            screen.blit(attr_text, (SCREEN_WIDTH // 2 + 50, start_y + i * 50))

            # Draw attribute value
            if attribute == "Color":
                value_text = self.color_names[self.selected_color]
            elif attribute == "Max Speed":
                value_text = f"{self.kart_config['max_speed']:.1f}"
            elif attribute == "Acceleration":
                value_text = f"{self.kart_config['acceleration']:.2f}"
            elif attribute == "Turn Speed":
                value_text = f"{self.kart_config['turn_speed']:.1f}"

            value_surface = self.font_small.render(value_text, True, color)
            screen.blit(value_surface, (SCREEN_WIDTH //
                        2 + 250, start_y + i * 50 + 5))

            # Draw adjustment arrows for selected attribute
            if i == self.selected_attribute:
                left_arrow = self.font_medium.render("<", True, ORANGE)
                right_arrow = self.font_medium.render(">", True, ORANGE)
                screen.blit(left_arrow, (SCREEN_WIDTH //
                            2 + 220, start_y + i * 50))
                screen.blit(right_arrow, (SCREEN_WIDTH //
                            2 + 350, start_y + i * 50))

        # Draw performance bars
        bar_y = 420
        bar_width = 200
        bar_height = 20

        attributes_with_values = [
            ("Speed", self.kart_config['max_speed'] / 12),
            ("Acceleration", self.kart_config['acceleration'] / 0.8),
            ("Handling", self.kart_config['turn_speed'] / 8)
        ]

        for i, (name, value) in enumerate(attributes_with_values):
            # Draw label
            label_text = self.font_small.render(name, True, WHITE)
            screen.blit(label_text, (SCREEN_WIDTH // 2 - 100, bar_y + i * 35))

            # Draw bar background
            bar_rect = pygame.Rect(SCREEN_WIDTH // 2 +
                                   20, bar_y + i * 35, bar_width, bar_height)
            pygame.draw.rect(screen, DARK_GRAY, bar_rect)

            # Draw bar fill
            fill_width = int(bar_width * value)
            fill_rect = pygame.Rect(
                SCREEN_WIDTH // 2 + 20, bar_y + i * 35, fill_width, bar_height)
            pygame.draw.rect(screen, GREEN, fill_rect)

            # Draw bar border
            pygame.draw.rect(screen, WHITE, bar_rect, 2)

        # Controls
        controls_text = self.font_small.render(
            "UP/DOWN: Navigate | LEFT/RIGHT: Adjust | ENTER: Save | ESC: Cancel", True, GRAY)
        controls_rect = controls_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(controls_text, controls_rect)
