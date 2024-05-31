import pygame
import time
import sys

import threading
import socket

from plugins import GrassPlugin
from src import assetManager, Camera, World, Player

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

        # Initialise Camera
        self.CAMERA = Camera(self.DISPLAY)

        # Fonts
        pygame.font.init()
        self.fonts = {
            'roboto': pygame.font.Font('assets/fonts/roboto.ttf', 20)
        }

        # Asset Manager
        self.ASSET_MANAGER = assetManager(tile_size=64)
        self.ASSET_MANAGER.add_tileset('assets/tilesets/grass.png', 'assets/tilesets/grass.txt') # Grass Tileset

        # PLugins
        self.gm = GrassPlugin('assets/grass', tile_size=64, stiffness=400, max_unique=5, place_range=[0, 1])
        self.gm.enable_ground_shadows(shadow_radius=4, shadow_color=(0, 0, 1), shadow_shift=(1, 2))
        self.PLUGINS = {
            'grass': self.gm
        }

        # Socket client
        self.client_socket = socket.socket()
        self.client_thread = threading.Thread(target=self.client_program)
        self.client_thread.start()

        # Initialise Player
        self.PLAYER = Player(0, 0, self.DISPLAY, self.CAMERA, self.PLUGINS, self.client_socket)

        # Initialise World
        self.WORLD = World(self.DISPLAY, self.CAMERA, self.PLAYER, self.ASSET_MANAGER, self.PLUGINS, tile_size=64)

    def resize(self, event):
        self.player.resize(self.DISPLAY)

    def end(self):
        self.GAME_RUNNING = 0
        pygame.quit()
        sys.exit()

    def client_program(self):
        host = '127.0.0.1'
        port = 8008

        self.client_socket.connect((host, port))

        while self.GAME_RUNNING:
            data = self.client_socket.recv(1024).decode()
            if not data:
                break
            
            string = data
            array = string.split(':')

            if array[0] == '0':
                print('Given ID:', array[1])

        print('Connection closed.')

        self.client_socket.close()

    def run(self):
        self.delta_start = time.time()
        
        while self.GAME_RUNNING:

            # Clear Screen
            self.DISPLAY.fill((0, 0, 0))

            # Calculate Delta Time
            self.delta_time = time.time() - self.delta_start
            self.delta_start = time.time()

            # Update World
            self.WORLD.update(self.delta_time, 0)

            # Update Player
            self.PLAYER.update(self.delta_time)

            # Display debug
            self.DISPLAY.blit(self.fonts['roboto'].render(f'{self.CLOCK.get_fps()}', False, (255, 255, 255)), (10,6))

            # Handle Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end()
                if event.type == pygame.VIDEORESIZE:
                    self.resize(event)

            # Update Frame
            pygame.display.flip()
            self.CLOCK.tick(2500)


if __name__ == "__main__":
    pygame.init()
    Game().run()