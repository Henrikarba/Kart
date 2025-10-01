"""
Base Scene class that all game scenes inherit from.
"""

import pygame


class Scene:
    def __init__(self, game):
        """Initialize the scene."""
        self.game = game

    def handle_event(self, event):
        """Handle pygame events."""
        pass

    def update(self, dt):
        """Update the scene."""
        pass

    def draw(self, screen):
        """Draw the scene."""
        pass

    def on_enter(self, **kwargs):
        """Called when entering this scene."""
        pass

    def on_exit(self):
        """Called when exiting this scene."""
        pass
