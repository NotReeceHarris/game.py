import pygame
import time
import sys

from .plugins import GrassPlugin

flags = pygame.RESIZABLE
window_size = (800,600)

class Game:
    def __init__(self):
        self.GAME_RUNNING = 1

        # Initialise Clock
        self.CLOCK = pygame.time.Clock()

        # Configure Display
        pygame.display.set_caption(f'farmer.py | v 0.1.0')

        # Initialise Display
        self.DISPLAY = pygame.display.set_mode(window_size, flags)

        # Fonts
        pygame.font.init()
        self.fonts = {
            'roboto': pygame.font.Font('assets/fonts/roboto.ttf', 20)
        }

        # PLugins
        self.gm = GrassPlugin('assets/grass', tile_size=self.tilesize, stiffness=1000, max_unique=5, place_range=[0, 1])
        self.gm.enable_ground_shadows(shadow_radius=4, shadow_color=(0, 0, 1), shadow_shift=(1, 2))
        self.plugins = {
            'grass': self.gm
        }

    def resize(self, event):
        pass

    def run(self):
        self.delta_start = time.time()
        
        while self.GAME_RUNNING:

            # Clear Screen
            self.DISPLAY.fill((0, 0, 0))

            # Calculate Delta Time
            self.delta_time = time.time() - self.delta_start
            self.delta_start = time.time()

            # Display debug
            self.DISPLAY.blit(self.fonts['roboto'].render(f'{self.CLOCK.get_fps()}', False, (255, 255, 255)), (10,6))

            # Handle Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.resize(event)

            # Update Frame
            pygame.display.flip()
            self.CLOCK.tick(2500)


if __name__ == "__main__":
    pygame.init()
    Game().run()