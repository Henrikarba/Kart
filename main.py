#!/usr/bin/env python3
"""
Mario Kart Style Racing Game
A simple racing game with AI opponents, multiple tracks, and kart customization.
"""

import pygame
import sys
from src.game import Game


def main():
    """Main entry point of the game."""
    pygame.init()

    # Create and run the game
    game = Game()
    game.run()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
