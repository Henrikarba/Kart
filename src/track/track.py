"""
Track class for creating racing tracks with checkpoints and hazards.
"""

import pygame
import math
from src.config import *


class Track:
    def __init__(self, track_id=0):
        """Initialize a track."""
        self.track_id = track_id
        self.checkpoints = []
        self.start_line = None
        self.track_surface = None
        self.water_areas = []
        self.track_boundaries = []

        # Track dimensions
        self.width = 2000
        self.height = 1500

        # Generate track based on ID
        self.generate_track()

    def generate_track(self):
        """Generate track layout based on track_id."""
        if self.track_id == 0:
            self.create_oval_track()
        elif self.track_id == 1:
            self.create_forest_track()
        elif self.track_id == 2:
            self.create_desert_track()
        else:
            self.create_oval_track()  # Default

    def create_oval_track(self):
        """Create a simple oval track."""
        # Track center and dimensions
        center_x, center_y = self.width // 2, self.height // 2
        outer_radius_x = 400
        outer_radius_y = 250
        inner_radius_x = 280
        inner_radius_y = 130

        # Create checkpoints around the oval
        num_checkpoints = 8
        self.checkpoints = []

        for i in range(num_checkpoints):
            angle = (i / num_checkpoints) * 2 * math.pi
            # Place checkpoints on the track centerline
            radius_x = (outer_radius_x + inner_radius_x) / 2
            radius_y = (outer_radius_y + inner_radius_y) / 2

            x = center_x + radius_x * math.cos(angle)
            y = center_y + radius_y * math.sin(angle)
            self.checkpoints.append((x, y))

        # Set start line (first checkpoint)
        self.start_line = self.checkpoints[0]

        # Create track surface
        self.track_surface = pygame.Surface((self.width, self.height))
        self.track_surface.fill(DARK_GREEN)  # Grass background

        # Draw track
        # Outer boundary
        pygame.draw.ellipse(self.track_surface, DARK_GRAY,
                            (center_x - outer_radius_x, center_y - outer_radius_y,
                             outer_radius_x * 2, outer_radius_y * 2))

        # Inner boundary (grass island)
        pygame.draw.ellipse(self.track_surface, DARK_GREEN,
                            (center_x - inner_radius_x, center_y - inner_radius_y,
                             inner_radius_x * 2, inner_radius_y * 2))

        # Draw track boundaries for collision detection
        self.track_boundaries = [
            # Outer ellipse
            (center_x, center_y, outer_radius_x, outer_radius_y, "outer"),
            # Inner ellipse
            (center_x, center_y, inner_radius_x, inner_radius_y, "inner")
        ]

        # Draw start line
        start_x, start_y = self.start_line
        pygame.draw.line(self.track_surface, WHITE,
                         (start_x - 30, start_y - 10), (start_x - 30, start_y + 10), 3)
        pygame.draw.line(self.track_surface, WHITE,
                         (start_x + 30, start_y - 10), (start_x + 30, start_y + 10), 3)

    def create_forest_track(self):
        """Create a winding forest track."""
        # Define track as a series of connected curves
        track_points = [
            (300, 300), (600, 200), (900, 300), (1200, 500),
            (1400, 800), (1200, 1100), (800, 1200), (400, 1100),
            (200, 800), (250, 500)
        ]

        self.checkpoints = track_points.copy()
        self.start_line = track_points[0]

        # Create track surface
        self.track_surface = pygame.Surface((self.width, self.height))
        self.track_surface.fill(DARK_GREEN)  # Forest background

        # Draw track segments
        for i in range(len(track_points)):
            start_point = track_points[i]
            end_point = track_points[(i + 1) % len(track_points)]

            # Draw thick line for track
            pygame.draw.line(self.track_surface, DARK_GRAY,
                             start_point, end_point, TRACK_WIDTH)

        # Add some water hazards
        self.water_areas = [
            (500, 600, 80),  # (x, y, radius)
            (1000, 400, 60),
            (700, 900, 70)
        ]

        for water_x, water_y, water_radius in self.water_areas:
            pygame.draw.circle(self.track_surface, WATER_BLUE,
                               (int(water_x), int(water_y)), water_radius)

        # Create track boundaries (simplified for winding track)
        self.track_boundaries = track_points

        # Draw start line
        start_x, start_y = self.start_line
        pygame.draw.line(self.track_surface, WHITE,
                         (start_x - 20, start_y - 15), (start_x - 20, start_y + 15), 3)
        pygame.draw.line(self.track_surface, WHITE,
                         (start_x + 20, start_y - 15), (start_x + 20, start_y + 15), 3)

    def create_desert_track(self):
        """Create a desert track with sand and water hazards."""
        # Figure-8 style track
        center_x, center_y = self.width // 2, self.height // 2

        # Define figure-8 checkpoints
        self.checkpoints = [
            (center_x - 200, center_y - 200),  # Top left
            (center_x, center_y - 250),       # Top center
            (center_x + 200, center_y - 200),  # Top right
            (center_x + 100, center_y),       # Center right
            (center_x + 200, center_y + 200),  # Bottom right
            (center_x, center_y + 250),       # Bottom center
            (center_x - 200, center_y + 200),  # Bottom left
            (center_x - 100, center_y)        # Center left
        ]

        self.start_line = self.checkpoints[0]

        # Create track surface
        self.track_surface = pygame.Surface((self.width, self.height))
        self.track_surface.fill(YELLOW)  # Sand background

        # Draw figure-8 track
        for i in range(len(self.checkpoints)):
            start_point = self.checkpoints[i]
            end_point = self.checkpoints[(i + 1) % len(self.checkpoints)]
            pygame.draw.line(self.track_surface, BROWN,
                             start_point, end_point, TRACK_WIDTH)

        # Add water hazards in center and corners
        self.water_areas = [
            (center_x, center_y, 40),           # Center
            (center_x - 300, center_y - 300, 50),  # Top left corner
            (center_x + 300, center_y + 300, 50)  # Bottom right corner
        ]

        for water_x, water_y, water_radius in self.water_areas:
            pygame.draw.circle(self.track_surface, WATER_BLUE,
                               (int(water_x), int(water_y)), water_radius)

        self.track_boundaries = self.checkpoints

        # Draw start line
        start_x, start_y = self.start_line
        pygame.draw.line(self.track_surface, WHITE,
                         (start_x - 25, start_y - 10), (start_x - 25, start_y + 10), 3)
        pygame.draw.line(self.track_surface, WHITE,
                         (start_x + 25, start_y - 10), (start_x + 25, start_y + 10), 3)

    def is_on_track(self, x, y):
        """Check if a position is on the track."""
        if not self.track_surface:
            return True

        # Check bounds
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return False

        # Get pixel color at position
        try:
            color = self.track_surface.get_at((int(x), int(y)))
            # Track is dark gray or brown
            return color in [DARK_GRAY, BROWN] or (color[0] < 100 and color[1] < 100 and color[2] < 100)
        except IndexError:
            return False

    def is_in_water(self, x, y):
        """Check if a position is in water (needs respawn)."""
        for water_x, water_y, water_radius in self.water_areas:
            distance = math.sqrt((x - water_x) ** 2 + (y - water_y) ** 2)
            if distance <= water_radius:
                return True
        return False

    def get_nearest_checkpoint(self, x, y):
        """Get the nearest checkpoint to a position."""
        if not self.checkpoints:
            return None

        min_distance = float('inf')
        nearest_checkpoint = None

        for checkpoint in self.checkpoints:
            distance = math.sqrt(
                (x - checkpoint[0]) ** 2 + (y - checkpoint[1]) ** 2)
            if distance < min_distance:
                min_distance = distance
                nearest_checkpoint = checkpoint

        return nearest_checkpoint

    def get_start_positions(self, num_karts):
        """Get starting positions for karts."""
        if not self.start_line:
            return [(100, 100) for _ in range(num_karts)]

        start_x, start_y = self.start_line
        positions = []

        # Arrange karts in a grid behind the start line
        for i in range(num_karts):
            row = i // 2
            col = i % 2

            offset_x = (col - 0.5) * 40  # Side by side spacing
            offset_y = -row * 50 - 50    # Behind start line

            positions.append((start_x + offset_x, start_y + offset_y))

        return positions

    def draw(self, screen, camera_x, camera_y):
        """Draw the track on screen with camera offset."""
        if self.track_surface:
            screen.blit(self.track_surface, (-camera_x, -camera_y))

        # Draw checkpoints for debugging (optional)
        for i, checkpoint in enumerate(self.checkpoints):
            screen_x = checkpoint[0] - camera_x
            screen_y = checkpoint[1] - camera_y

            # Only draw if on screen
            if -50 < screen_x < SCREEN_WIDTH + 50 and -50 < screen_y < SCREEN_HEIGHT + 50:
                pygame.draw.circle(
                    screen, GREEN, (int(screen_x), int(screen_y)), CHECKPOINT_RADIUS, 3)

                # Draw checkpoint number
                font = pygame.font.Font(None, 24)
                text = font.render(str(i), True, WHITE)
                screen.blit(text, (screen_x - 5, screen_y - 10))
