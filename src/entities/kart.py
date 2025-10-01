"""
Kart class representing a racing kart with physics and controls.
"""

import pygame
import math
from src.config import *


class Kart:
    def __init__(self, x, y, color=RED, is_player=False, config=None):
        """Initialize a kart."""
        self.x = x
        self.y = y
        self.angle = 0  # Rotation angle in degrees
        self.speed = 0
        self.color = color
        self.is_player = is_player

        # Kart configuration
        if config:
            self.max_speed = config.get('max_speed', MAX_SPEED)
            self.acceleration = config.get('acceleration', ACCELERATION)
            self.turn_speed = config.get('turn_speed', TURN_SPEED)
        else:
            self.max_speed = MAX_SPEED
            self.acceleration = ACCELERATION
            self.turn_speed = TURN_SPEED

        # Physics properties
        self.velocity_x = 0
        self.velocity_y = 0
        self.friction = 0.95

        # Race tracking
        self.current_lap = 0
        self.last_checkpoint = -1
        self.race_position = 0
        self.finished = False
        self.finish_time = 0

        # Respawn
        self.respawn_x = x
        self.respawn_y = y
        self.respawn_angle = 0

        # Off-track status
        self.on_track = True

        # Create kart surface
        self.size = KART_SIZE
        self.create_kart_surface()

    def create_kart_surface(self):
        """Create the visual representation of the kart."""
        self.original_surface = pygame.Surface(
            (self.size, self.size), pygame.SRCALPHA)

        # Draw kart body (rectangle)
        body_rect = pygame.Rect(2, 2, self.size - 4, self.size - 4)
        pygame.draw.rect(self.original_surface, self.color, body_rect)
        pygame.draw.rect(self.original_surface, BLACK, body_rect, 2)

        # Draw direction indicator (small triangle at front)
        front_triangle = [
            (self.size - 2, self.size // 2),
            (self.size - 8, self.size // 2 - 3),
            (self.size - 8, self.size // 2 + 3)
        ]
        pygame.draw.polygon(self.original_surface, BLACK, front_triangle)

        self.surface = self.original_surface.copy()

    def update(self, dt, track=None):
        """Update kart physics and movement."""
        # Handle input for player kart
        if self.is_player:
            self.handle_input(dt)

        # Apply friction
        self.speed *= self.friction

        # Calculate velocity based on angle and speed
        angle_rad = math.radians(self.angle)
        self.velocity_x = math.cos(angle_rad) * self.speed
        self.velocity_y = math.sin(angle_rad) * self.speed

        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Check track boundaries if track is provided
        if track:
            self.on_track = track.is_on_track(self.x, self.y)

            # Apply speed penalty if off track
            if not self.on_track:
                self.speed *= OFF_TRACK_SPEED_PENALTY

            # Check for water hazards (respawn)
            if track.is_in_water(self.x, self.y):
                self.respawn()

        # Rotate the kart surface
        self.surface = pygame.transform.rotate(
            self.original_surface, -self.angle)

    def handle_input(self, dt):
        """Handle player input."""
        keys = pygame.key.get_pressed()

        # Acceleration and deceleration
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.speed = max(self.speed - self.acceleration *
                             2, -self.max_speed * 0.5)
        else:
            # Natural deceleration when no input
            if self.speed > 0:
                self.speed = max(0, self.speed - DECELERATION * dt)
            elif self.speed < 0:
                self.speed = min(0, self.speed + DECELERATION * dt)

        # Turning (only when moving)
        if abs(self.speed) > 0.1:
            turning_factor = min(abs(self.speed) / self.max_speed, 1.0)

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.angle -= self.turn_speed * turning_factor
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.angle += self.turn_speed * turning_factor

    def respawn(self):
        """Respawn the kart at the last checkpoint."""
        self.x = self.respawn_x
        self.y = self.respawn_y
        self.angle = self.respawn_angle
        self.speed = 0
        self.velocity_x = 0
        self.velocity_y = 0

    def set_respawn_point(self, x, y, angle):
        """Set a new respawn point (usually at a checkpoint)."""
        self.respawn_x = x
        self.respawn_y = y
        self.respawn_angle = angle

    def get_rect(self):
        """Get the bounding rectangle of the kart."""
        return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)

    def get_center(self):
        """Get the center position of the kart."""
        return (self.x, self.y)

    def draw(self, screen, camera_x=0, camera_y=0):
        """Draw the kart on the screen."""
        # Calculate screen position accounting for camera
        screen_x = self.x - camera_x - self.surface.get_width() // 2
        screen_y = self.y - camera_y - self.surface.get_height() // 2

        screen.blit(self.surface, (screen_x, screen_y))

        # Draw debug info for player
        if self.is_player:
            font = pygame.font.Font(None, 24)
            speed_text = font.render(f"Speed: {self.speed:.1f}", True, WHITE)
            screen.blit(speed_text, (10, 10))

            position_text = font.render(
                f"Position: {self.race_position}", True, WHITE)
            screen.blit(position_text, (10, 35))

            lap_text = font.render(
                f"Lap: {self.current_lap + 1}/{TOTAL_LAPS}", True, WHITE)
            screen.blit(lap_text, (10, 60))
