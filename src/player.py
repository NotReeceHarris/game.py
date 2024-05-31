import math
import pygame

SQRT_2 = math.sqrt(2)

class Player:
    def __init__(self, x, y, display, camera, plugins, socket):
        self.width = 10
        self.height = 10
        self.display = display
        self.camera = camera
        self.socket = socket
        
        self.x = x
        self.y = y

        self.w, self.h = pygame.display.get_surface().get_size()

        self.base_speed = 100
        self.speed = self.base_speed
        self.speed_multiplier = 1.25
        self.direction = 'down'

        self.plugins = plugins

        # Mapping keys to directions and velocities
        self.key_directions = {
            pygame.K_LEFT: ('left', -self.speed, 0),
            pygame.K_a: ('left', -self.speed, 0),
            pygame.K_RIGHT: ('right', self.speed, 0),
            pygame.K_d: ('right', self.speed, 0),
            pygame.K_UP: ('up', 0, -self.speed),
            pygame.K_w: ('up', 0, -self.speed),
            pygame.K_DOWN: ('down', 0, self.speed),
            pygame.K_s: ('down', 0, self.speed),
        }

    def position(self):
        return self.x, self.y

    def set_position(self, x, y):
        self.x = x
        self.y = y
    
    def resize(self, display):
        self.w, self.h = pygame.display.get_surface().get_size()
        self.display = display

    def move(self, dt):
        keys = pygame.key.get_pressed()
        new_character_x, new_character_y = self.x, self.y
        velocity_x, velocity_y = 0, 0

        # Handle key presses
        for key in (k for k in self.key_directions if keys[k]):
            direction, vx, vy = self.key_directions[key]

            self.direction = direction
            velocity_x += vx
            velocity_y += vy

        # Diagonal movement
        if velocity_x != 0 and velocity_y != 0:
            velocity_x /= SQRT_2
            velocity_y /= SQRT_2

        new_character_x += velocity_x*dt 
        new_character_y += velocity_y*dt

        if self.x != new_character_x or self.y != new_character_y:
            self.socket.send(f'1:{new_character_x}:{new_character_y}'.encode())

        return new_character_x, new_character_y

    def update(self, dt):

        # Movement
        self.new_character_x, self.new_character_y = self.move(dt)

        self.x = self.new_character_x
        self.y = self.new_character_y

        # Frame updates
        self.camera.set_offset(self.x - self.w // 2, self.y - self.h // 2)
        pygame.draw.rect(self.display, (0, 0, 255), (self.w // 2, self.h // 2, self.width, self.height))
        self.plugins['grass'].apply_force((self.x, self.y), 20, 35)