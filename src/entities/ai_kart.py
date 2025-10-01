"""
AI Kart class that extends the base Kart with artificial intelligence.
"""

import pygame
import math
import random
from src.entities.kart import Kart
from src.config import *


class AIKart(Kart):
    def __init__(self, x, y, color=BLUE, config=None, track=None):
        """Initialize an AI-controlled kart."""
        super().__init__(x, y, color, is_player=False, config=config)

        self.track = track
        self.target_point = None
        self.reaction_timer = 0
        self.ai_speed_multiplier = random.uniform(
            0.8, 1.0)  # Add variety to AI performance

        # AI behavior parameters
        self.look_ahead_distance = 100
        self.max_turn_angle = 45  # Maximum turn per frame
        self.stuck_timer = 0
        self.stuck_threshold = 3.0  # Seconds before considering stuck
        self.last_position = (x, y)
        self.stuck_check_timer = 0

        # Pathfinding
        self.waypoints = []
        self.current_waypoint = 0

        if track:
            self.generate_waypoints()

    def generate_waypoints(self):
        """Generate waypoints along the track for AI to follow."""
        if not self.track or not hasattr(self.track, 'checkpoints'):
            return

        # Use track checkpoints as base waypoints
        self.waypoints = []
        checkpoints = self.track.checkpoints

        for i in range(len(checkpoints)):
            checkpoint = checkpoints[i]
            # Add some variation to make AI look more natural
            offset_x = random.uniform(-20, 20)
            offset_y = random.uniform(-20, 20)
            self.waypoints.append(
                (checkpoint[0] + offset_x, checkpoint[1] + offset_y))

    def update(self, dt, track=None):
        """Update AI kart with intelligent behavior."""
        self.reaction_timer += dt
        self.stuck_check_timer += dt

        # Check if stuck
        if self.stuck_check_timer > 1.0:  # Check every second
            current_pos = (self.x, self.y)
            distance_moved = math.sqrt(
                (current_pos[0] - self.last_position[0]) ** 2 +
                (current_pos[1] - self.last_position[1]) ** 2
            )

            if distance_moved < 10:  # Barely moved
                self.stuck_timer += self.stuck_check_timer
            else:
                self.stuck_timer = 0

            self.last_position = current_pos
            self.stuck_check_timer = 0

        # If stuck for too long, respawn
        if self.stuck_timer > self.stuck_threshold:
            self.respawn()
            self.stuck_timer = 0

        # AI decision making (with reaction delay)
        if self.reaction_timer >= AI_REACTION_TIME:
            self.make_ai_decisions(dt)
            self.reaction_timer = 0

        # Update physics
        super().update(dt, track)

    def make_ai_decisions(self, dt):
        """Make AI decisions for movement and steering."""
        if not self.waypoints:
            # Fallback: just go forward
            self.speed = min(self.speed + self.acceleration,
                             self.max_speed * self.ai_speed_multiplier)
            return

        # Find target waypoint
        target_waypoint = self.get_target_waypoint()

        if target_waypoint:
            # Calculate angle to target
            dx = target_waypoint[0] - self.x
            dy = target_waypoint[1] - self.y
            target_angle = math.degrees(math.atan2(dy, dx))

            # Calculate angle difference
            angle_diff = target_angle - self.angle

            # Normalize angle difference to [-180, 180]
            while angle_diff > 180:
                angle_diff -= 360
            while angle_diff < -180:
                angle_diff += 360

            # Determine turning direction and speed
            if abs(angle_diff) > 5:  # Need to turn
                turn_amount = min(abs(angle_diff), self.max_turn_angle)
                if angle_diff > 0:
                    self.angle += turn_amount * 0.1  # Smooth turning
                else:
                    self.angle -= turn_amount * 0.1

            # Adjust speed based on turn sharpness
            if abs(angle_diff) > 30:
                # Sharp turn, slow down
                target_speed = self.max_speed * 0.6 * self.ai_speed_multiplier
            elif abs(angle_diff) > 15:
                # Moderate turn
                target_speed = self.max_speed * 0.8 * self.ai_speed_multiplier
            else:
                # Straight or gentle turn, full speed
                target_speed = self.max_speed * self.ai_speed_multiplier

            # Accelerate or decelerate towards target speed
            if self.speed < target_speed:
                self.speed = min(self.speed + self.acceleration, target_speed)
            elif self.speed > target_speed:
                self.speed = max(
                    self.speed - self.acceleration * 2, target_speed)

    def get_target_waypoint(self):
        """Get the current target waypoint."""
        if not self.waypoints:
            return None

        # Check if we've reached the current waypoint
        current_waypoint = self.waypoints[self.current_waypoint]
        distance_to_waypoint = math.sqrt(
            (current_waypoint[0] - self.x) ** 2 +
            (current_waypoint[1] - self.y) ** 2
        )

        # If close to waypoint, advance to next one
        if distance_to_waypoint < 50:
            self.current_waypoint = (
                self.current_waypoint + 1) % len(self.waypoints)
            current_waypoint = self.waypoints[self.current_waypoint]

        return current_waypoint

    def handle_input(self, dt):
        """Override parent method - AI doesn't use input."""
        pass

    def draw(self, screen, camera_x=0, camera_y=0):
        """Draw the AI kart."""
        super().draw(screen, camera_x, camera_y)

        # Draw waypoint for debugging (optional)
        if self.waypoints and hasattr(self, 'debug_mode') and self.debug_mode:
            target = self.get_target_waypoint()
            if target:
                screen_x = target[0] - camera_x
                screen_y = target[1] - camera_y
                pygame.draw.circle(
                    screen, YELLOW, (int(screen_x), int(screen_y)), 5)
