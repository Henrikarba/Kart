"""
Main Game Scene where the racing happens.
"""

import pygame
import math
from src.scenes.base_scene import Scene
from src.config import *
from src.entities.kart import Kart
from src.entities.ai_kart import AIKart
from src.track.track import Track


class GameScene(Scene):
    def __init__(self, game, selected_track=0):
        super().__init__(game)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Game state
        self.paused = False
        self.race_started = False
        self.race_finished = False
        self.countdown_timer = 3.0
        self.race_timer = 0.0

        # Create track
        self.track = Track(selected_track)

        # Create karts
        self.karts = []
        start_positions = self.track.get_start_positions(4)  # Player + 3 AI

        # Player kart
        player_pos = start_positions[0]
        self.player_kart = Kart(
            player_pos[0], player_pos[1],
            color=self.game.player_kart_config['color'],
            is_player=True,
            config=self.game.player_kart_config
        )
        self.karts.append(self.player_kart)

        # AI karts
        ai_colors = [BLUE, GREEN, PURPLE]
        for i in range(3):
            ai_pos = start_positions[i + 1]
            ai_kart = AIKart(
                ai_pos[0], ai_pos[1],
                color=ai_colors[i],
                track=self.track
            )
            self.karts.append(ai_kart)

        # Camera
        self.camera_x = 0
        self.camera_y = 0

        # Race management
        self.race_manager = RaceManager(self.karts, self.track)

        # Set initial respawn points
        for kart in self.karts:
            if self.track.start_line:
                kart.set_respawn_point(
                    self.track.start_line[0], self.track.start_line[1], 0)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
            elif event.key == pygame.K_r and (self.paused or self.race_finished):
                # Restart race
                self.restart_race()
            elif event.key == pygame.K_m and (self.paused or self.race_finished):
                # Return to menu
                self.game.change_state(MENU)

    def restart_race(self):
        """Restart the current race."""
        # Reset race state
        self.race_started = False
        self.race_finished = False
        self.countdown_timer = 3.0
        self.race_timer = 0.0
        self.paused = False

        # Reset all karts
        start_positions = self.track.get_start_positions(len(self.karts))
        for i, kart in enumerate(self.karts):
            pos = start_positions[i]
            kart.x = pos[0]
            kart.y = pos[1]
            kart.angle = 0
            kart.speed = 0
            kart.velocity_x = 0
            kart.velocity_y = 0
            kart.current_lap = 0
            kart.last_checkpoint = -1
            kart.finished = False
            kart.finish_time = 0

            if self.track.start_line:
                kart.set_respawn_point(
                    self.track.start_line[0], self.track.start_line[1], 0)

        # Reset race manager
        self.race_manager.reset_race()

    def update(self, dt):
        if self.paused:
            return

        # Handle countdown
        if not self.race_started:
            self.countdown_timer -= dt
            if self.countdown_timer <= 0:
                self.race_started = True

        # Update race timer
        if self.race_started and not self.race_finished:
            self.race_timer += dt

        # Update karts only if race has started
        if self.race_started:
            for kart in self.karts:
                kart.update(dt, self.track)

            # Update race management
            self.race_manager.update(dt)

            # Check for race finish
            if self.race_manager.is_race_finished():
                self.race_finished = True

        # Update camera to follow player
        self.update_camera()

    def update_camera(self):
        """Update camera to follow the player kart."""
        target_x = self.player_kart.x - SCREEN_WIDTH // 2
        target_y = self.player_kart.y - SCREEN_HEIGHT // 2

        # Smooth camera movement
        self.camera_x += (target_x - self.camera_x) * 0.1
        self.camera_y += (target_y - self.camera_y) * 0.1

        # Keep camera within track bounds
        self.camera_x = max(
            0, min(self.camera_x, self.track.width - SCREEN_WIDTH))
        self.camera_y = max(
            0, min(self.camera_y, self.track.height - SCREEN_HEIGHT))

    def draw(self, screen):
        # Draw track
        self.track.draw(screen, self.camera_x, self.camera_y)

        # Draw karts
        for kart in self.karts:
            kart.draw(screen, self.camera_x, self.camera_y)

        # Draw UI
        self.draw_ui(screen)

        # Draw countdown
        if not self.race_started:
            self.draw_countdown(screen)

        # Draw pause screen
        if self.paused:
            self.draw_pause_screen(screen)

        # Draw race results
        if self.race_finished:
            self.draw_race_results(screen)

    def draw_ui(self, screen):
        """Draw the game UI."""
        # Race info
        if self.race_started:
            # Timer
            time_text = f"Time: {self.race_timer:.1f}s"
            time_surface = self.small_font.render(time_text, True, WHITE)
            screen.blit(time_surface, (SCREEN_WIDTH - 150, 10))

            # Player position
            position_text = f"Position: {self.player_kart.race_position}"
            position_surface = self.small_font.render(
                position_text, True, WHITE)
            screen.blit(position_surface, (SCREEN_WIDTH - 150, 35))

            # Player lap
            lap_text = f"Lap: {self.player_kart.current_lap + 1}/{TOTAL_LAPS}"
            lap_surface = self.small_font.render(lap_text, True, WHITE)
            screen.blit(lap_surface, (SCREEN_WIDTH - 150, 60))

        # Speed (always show for player)
        speed_text = f"Speed: {self.player_kart.speed:.1f}"
        speed_surface = self.small_font.render(speed_text, True, WHITE)
        screen.blit(speed_surface, (10, 10))

        # Controls hint
        controls_text = "WASD/Arrows: Move | ESC: Pause"
        controls_surface = self.small_font.render(controls_text, True, GRAY)
        screen.blit(controls_surface, (10, SCREEN_HEIGHT - 30))

    def draw_countdown(self, screen):
        """Draw countdown before race starts."""
        if self.countdown_timer > 0:
            count = int(self.countdown_timer) + 1
            countdown_text = str(count)
        else:
            countdown_text = "GO!"

        countdown_surface = self.font.render(countdown_text, True, YELLOW)
        countdown_rect = countdown_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # Draw background
        bg_rect = countdown_rect.inflate(40, 20)
        pygame.draw.rect(screen, BLACK, bg_rect)
        pygame.draw.rect(screen, WHITE, bg_rect, 3)

        screen.blit(countdown_surface, countdown_rect)

    def draw_pause_screen(self, screen):
        """Draw pause screen overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # Pause text
        pause_text = self.font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(pause_text, pause_rect)

        # Instructions
        instructions = [
            "ESC - Resume",
            "R - Restart Race",
            "M - Main Menu"
        ]

        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, WHITE)
            text_rect = text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 30))
            screen.blit(text, text_rect)

    def draw_race_results(self, screen):
        """Draw race results screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # Results title
        if self.player_kart.race_position == 1:
            title_text = "VICTORY!"
            title_color = YELLOW
        else:
            title_text = "RACE FINISHED"
            title_color = WHITE

        title_surface = self.font.render(title_text, True, title_color)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(title_surface, title_rect)

        # Player results
        result_text = f"Final Position: {self.player_kart.race_position}"
        result_surface = self.small_font.render(result_text, True, WHITE)
        result_rect = result_surface.get_rect(center=(SCREEN_WIDTH // 2, 250))
        screen.blit(result_surface, result_rect)

        time_text = f"Race Time: {self.race_timer:.1f}s"
        time_surface = self.small_font.render(time_text, True, WHITE)
        time_rect = time_surface.get_rect(center=(SCREEN_WIDTH // 2, 280))
        screen.blit(time_surface, time_rect)

        # Instructions
        instructions = [
            "R - Restart Race",
            "M - Main Menu"
        ]

        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 350 + i * 30))
            screen.blit(text, text_rect)


class RaceManager:
    """Manages race logic including laps, checkpoints, and positions."""

    def __init__(self, karts, track):
        self.karts = karts
        self.track = track
        self.total_laps = TOTAL_LAPS

    def update(self, dt):
        """Update race management."""
        self.update_checkpoints()
        self.update_positions()

    def update_checkpoints(self):
        """Update checkpoint progress for all karts."""
        for kart in self.karts:
            if kart.finished:
                continue

            # Check each checkpoint
            for i, checkpoint in enumerate(self.track.checkpoints):
                distance = math.sqrt(
                    (kart.x - checkpoint[0]) ** 2 +
                    (kart.y - checkpoint[1]) ** 2
                )

                if distance < CHECKPOINT_RADIUS:
                    # Check if this is the next expected checkpoint
                    expected_checkpoint = (
                        kart.last_checkpoint + 1) % len(self.track.checkpoints)

                    if i == expected_checkpoint:
                        kart.last_checkpoint = i

                        # Update respawn point
                        kart.set_respawn_point(
                            checkpoint[0], checkpoint[1], kart.angle)

                        # Check for lap completion
                        if i == 0 and kart.last_checkpoint == 0 and kart.current_lap > 0:
                            # Crossed start line, lap completed
                            kart.current_lap += 1

                            # Check for race completion
                            if kart.current_lap >= self.total_laps:
                                kart.finished = True
                                kart.finish_time = pygame.time.get_ticks() / 1000.0
                        elif i == 0 and kart.current_lap == 0:
                            # First time crossing start line
                            kart.current_lap = 1

    def update_positions(self):
        """Update race positions for all karts."""
        # Sort karts by race progress
        def get_race_progress(kart):
            if kart.finished:
                # Finished karts first
                return 1000 + (self.total_laps - kart.finish_time)
            else:
                return kart.current_lap * len(self.track.checkpoints) + kart.last_checkpoint + 1

        sorted_karts = sorted(self.karts, key=get_race_progress, reverse=True)

        for i, kart in enumerate(sorted_karts):
            kart.race_position = i + 1

    def is_race_finished(self):
        """Check if the race is finished."""
        finished_karts = sum(1 for kart in self.karts if kart.finished)
        # Race ends when player finishes
        return finished_karts >= len(self.karts) or self.karts[0].finished

    def reset_race(self):
        """Reset race state."""
        for kart in self.karts:
            kart.current_lap = 0
            kart.last_checkpoint = -1
            kart.race_position = 1
            kart.finished = False
            kart.finish_time = 0
