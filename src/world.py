import pygame
import math
import random

from src.noise import grassMap

# Chunk size must be even
CHUNK_SIZE_Y = 16
CHUNK_SIZE_X = 16
CHUNK_DUMP_D = 5

# Settings
USE_DYNAMIC_GRASS = True

class World:
    def __init__(self, display, camera, player, tilesets, plugins, tile_size):
        self.display = display
        self.camera = camera
        self.player = player
        self.tilesets = tilesets
        self.plugins = plugins
        self.tile_size = tile_size

        self.w, self.h = pygame.display.get_surface().get_size()

        self.loaded_chunks = {}
        self.visible_chunks = []

        self.SPACE_X = (self.w / 2) + self.tile_size
        self.SPACE_Y = (self.h / 2) + self.tile_size

        self.CURRENT_CHUNK = None

        self.CHUNKS_X = math.ceil(self.SPACE_X / (CHUNK_SIZE_X * self.tile_size))
        self.CHUNKS_Y = math.ceil(self.SPACE_Y / (CHUNK_SIZE_X * self.tile_size))

        self.CHUNK_SIZE_X_PX = self.tile_size * CHUNK_SIZE_X
        self.CHUNK_SIZE_Y_PX = self.tile_size * CHUNK_SIZE_Y

        self.t = 0
        self.offsets = {(0, 0)}

    def resize(self, display):
        self.w, self.h = pygame.display.get_surface().get_size()
        self.SPACE_X = (self.w / 2) + self.tile_size
        self.SPACE_Y = (self.h / 2) + self.tile_size
        self.CHUNKS_X = math.ceil(self.SPACE_X / (CHUNK_SIZE_X * self.tile_size))
        self.CHUNKS_Y = math.ceil(self.SPACE_Y / (CHUNK_SIZE_X * self.tile_size))
        self.get_visible_chunks()
        self.display = display
        return
    
    def generate_chunks(self, chunk_x, chunk_y):
        """ 
        Generates a chunk based on the given chunk coordinates (chunk_x, chunk_y).
        This function creates 7 surfaces for a single chunk, each representing a different
        animation frame. These 7 surfaces are displayed sequentially to animate the chunk.

        Previously, the code generated each chunk individually in a loop, which was slow.
        The current implementation generates all 7 chunks simultaneously, significantly 
        reducing processing time and improving efficiency.
        """

        chunk_size = CHUNK_SIZE_X * self.tile_size
        rect = pygame.FRect(0, 0, self.tile_size, self.tile_size)

        chunks = [
            pygame.Surface(( chunk_size, chunk_size )),
            pygame.Surface(( chunk_size, chunk_size )),
            pygame.Surface(( chunk_size, chunk_size )),
            pygame.Surface(( chunk_size, chunk_size )),
            pygame.Surface(( chunk_size, chunk_size )),
            pygame.Surface(( chunk_size, chunk_size )),
            pygame.Surface(( chunk_size, chunk_size ))
        ]

        tiles = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        ]

        for y in range(CHUNK_SIZE_Y):
            for x in range(CHUNK_SIZE_X):
                
                rect.x = x * self.tile_size 
                rect.y = y * self.tile_size 

                # Get the tile position in the world
                tile_x = x + chunk_x * CHUNK_SIZE_X
                tile_y = y + chunk_y * CHUNK_SIZE_Y

                # Define the tiles
                tile0 = tile1 = tile2 = tile3 = tile4 = tile5 = tile6 = None

                """ # Get the noise value for the tile
                water_noise = WaterMap(tile_x, tile_y, self.seed)
                is_water = water_noise == 0
                
                if is_water:
                    tile0 = self.tilesets['water']['frame_0']
                    tile1 = self.tilesets['water']['frame_1']
                    tile2 = self.tilesets['water']['frame_2']
                    tile3 = self.tilesets['water']['frame_3']
                    tile4 = self.tilesets['water']['frame_4']
                    tile5 = self.tilesets['water']['frame_5']
                    tile6 = self.tilesets['water']['frame_6']
                else:
                    # Check Water Map to texture water banks
                    water_right_tile = WaterMap(tile_x + 1, tile_y, self.seed) == 0
                    water_left_tile = WaterMap(tile_x - 1, tile_y, self.seed) == 0
                    water_top_tile = WaterMap(tile_x, tile_y - 1, self.seed) == 0
                    water_bottom_tile = WaterMap(tile_x, tile_y + 1, self.seed) == 0
                    water_bank_tile = self.water_bank_lookup_table.get((water_right_tile, water_bottom_tile, water_left_tile, water_top_tile))

                    water_corner_ne_tile = WaterMap(tile_x + 1, tile_y - 1, self.seed) == 0
                    water_corner_se_tile = WaterMap(tile_x + 1, tile_y + 1, self.seed) == 0
                    water_corner_sw_tile = WaterMap(tile_x - 1, tile_y + 1, self.seed) == 0
                    water_corner_nw_tile = WaterMap(tile_x - 1, tile_y - 1, self.seed) == 0
                    water_bank_corner_tile = self.water_bank_corner_lookup_table.get((water_corner_ne_tile, water_corner_se_tile, water_corner_sw_tile, water_corner_nw_tile))
                    
                    # Water bank tiles (edge of water).
                    if water_bank_tile != None:
                        tile0 = water_bank_tile['frame_0']
                        tile1 = water_bank_tile['frame_1']
                        tile2 = water_bank_tile['frame_2']
                        tile3 = water_bank_tile['frame_3']
                        tile4 = water_bank_tile['frame_4']
                        tile5 = water_bank_tile['frame_5']
                        tile6 = water_bank_tile['frame_6']
                    
                    # Water bank corner tiles (corner of water).
                    elif water_bank_corner_tile != None:
                        tile0 = water_bank_corner_tile['frame_0']
                        tile1 = water_bank_corner_tile['frame_1']
                        tile2 = water_bank_corner_tile['frame_2']
                        tile3 = water_bank_corner_tile['frame_3']
                        tile4 = water_bank_corner_tile['frame_4']
                        tile5 = water_bank_corner_tile['frame_5']
                        tile6 = water_bank_corner_tile['frame_6']
                """

                # If tiles havent been set make it grass.
                if tile0 == None:
                    if USE_DYNAMIC_GRASS:
                        grass_level = grassMap(tile_x, tile_y)

                        if grass_level <= -0.25:
                            self.plugins['grass'].place_tile((tile_x, tile_y), random.randint(15, 25), [0, 1, 2, 3, 4, 5])
                        elif grass_level <= -0.18:
                            self.plugins['grass'].place_tile((tile_x, tile_y), random.randint(5, 10), [0, 1, 2, 3, 4, 5])
                        elif grass_level <= -0.1:
                            self.plugins['grass'].place_tile((tile_x, tile_y), random.randint(1, 5), [0, 1, 2, 3, 4, 5])

                        tile0 = tile1 = tile2 = tile3 = tile4 = tile5 = tile6 = self.tilesets.get('grass')
                    else:
                        tile0 = tile1 = tile2 = tile3 = tile4 = tile5 = tile6 = random.choice(self.tilesets_grass)

                tiles[0].append((tile0, (rect.x, rect.y)))
                tiles[1].append((tile1, (rect.x, rect.y)))
                tiles[2].append((tile2, (rect.x, rect.y)))
                tiles[3].append((tile3, (rect.x, rect.y)))
                tiles[4].append((tile4, (rect.x, rect.y)))
                tiles[5].append((tile5, (rect.x, rect.y)))
                tiles[6].append((tile6, (rect.x, rect.y)))

        chunks[0].blits(tiles[0])
        chunks[1].blits(tiles[1])
        chunks[2].blits(tiles[2])
        chunks[3].blits(tiles[3])
        chunks[4].blits(tiles[4])
        chunks[5].blits(tiles[5])
        chunks[6].blits(tiles[6])

        return chunks


    def update(self, dt, anim_frame):
        CURRENT_CHUNK_X = math.floor(self.player.x / (CHUNK_SIZE_X * self.tile_size))
        CURRENT_CHUNK_Y = math.floor(self.player.y / (CHUNK_SIZE_Y * self.tile_size))
        IN_NEW_CHUNK = self.CURRENT_CHUNK != (CURRENT_CHUNK_X, CURRENT_CHUNK_Y)

        # Dump loaded chunks that are "DUMP_CHUNKS_DISTANCE" chunks away from the player visible chunks

        if IN_NEW_CHUNK:
            self.CURRENT_CHUNK = (CURRENT_CHUNK_X, CURRENT_CHUNK_Y)
            for chunk in list(self.loaded_chunks):
                if chunk[0] < CURRENT_CHUNK_X - CHUNK_DUMP_D or \
                    chunk[0] > CURRENT_CHUNK_X + CHUNK_DUMP_D or \
                    chunk[1] < CURRENT_CHUNK_Y - CHUNK_DUMP_D or \
                    chunk[1] > CURRENT_CHUNK_Y + CHUNK_DUMP_D:
                    del self.loaded_chunks[chunk]
        
        self.visible_chunks = []

        for offset_x, offset_y in self.offsets:
            new_chunk_x = CURRENT_CHUNK_X + offset_x
            new_chunk_y = CURRENT_CHUNK_Y + offset_y

            if (new_chunk_x, new_chunk_y) not in self.loaded_chunks:
                self.loaded_chunks[(new_chunk_x, new_chunk_y)] = self.generate_chunks(new_chunk_x, new_chunk_y)

            self.visible_chunks.append((
                self.loaded_chunks[(new_chunk_x, new_chunk_y)][anim_frame],
                (
                    (new_chunk_x * self.CHUNK_SIZE_X_PX) - self.camera.offset_x, 
                    (new_chunk_y * self.CHUNK_SIZE_Y_PX) - self.camera.offset_y
                )
            ))

        self.display.blits(self.visible_chunks)

        # Render Grass
        rot_function = lambda x, y: int(math.sin(self.t / 60 + x / 100) * 15)
        self.plugins['grass'].update_render(self.display, dt, offset=(self.camera.offset_x, self.camera.offset_y), rot_function=rot_function)
        self.t += dt * 45

        return