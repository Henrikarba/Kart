"""
Main Game class that handles the game loop and state management.
"""

import pygame
import sys
from src.config import *
from src.scenes.menu import MenuScene
from src.scenes.game_scene import GameScene
from src.scenes.customization import CustomizationScene
from src.scenes.track_select import TrackSelectScene


class Game:
    def __init__(self):
        """Initialize the game."""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mario Kart Style Racing Game")
        self.clock = pygame.time.Clock()
        self.running = True

        # Game state
        self.state = MENU
        self.selected_track = 0
        self.player_kart_config = {
            'color': RED,
            'max_speed': MAX_SPEED,
            'acceleration': ACCELERATION,
            'turn_speed': TURN_SPEED
        }

        # Initialize scenes
        self.scenes = {
            MENU: MenuScene(self),
            PLAYING: None,  # Will be created when needed
            CUSTOMIZATION: CustomizationScene(self),
            TRACK_SELECT: TrackSelectScene(self)
        }

        self.current_scene = self.scenes[MENU]

    def change_state(self, new_state, **kwargs):
        """Change the game state."""
        self.state = new_state

        # Create game scene when needed
        if new_state == PLAYING:
            if PLAYING not in self.scenes or self.scenes[PLAYING] is None:
                self.scenes[PLAYING] = GameScene(self, self.selected_track)
            else:
                # Reset the game scene
                self.scenes[PLAYING] = GameScene(self, self.selected_track)

        self.current_scene = self.scenes[new_state]

        # Handle any additional parameters
        if hasattr(self.current_scene, 'on_enter'):
            self.current_scene.on_enter(**kwargs)

    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.current_scene.handle_event(event)

            # Update current scene
            self.current_scene.update(dt)

            # Draw current scene
            self.screen.fill(BLACK)
            self.current_scene.draw(self.screen)

            pygame.display.flip()

    def quit_game(self):
        """Quit the game."""
        self.running = False
