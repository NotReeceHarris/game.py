import pygame


class assetManager:
    def __init__ (self, tile_size=64):
        self.tile_size = tile_size
        self.tiles = {}
        pass

    def add_tileset(self, path_path, data_path):
        """ 
        Add a tileset to the asset manager

        Args:
            path_path (str): The path to the tileset image
            data_path (str): The path to the tileset data (this tells the asset manager how to interpret the image file)

        Returns:
            None
        """
        
        tile_image = pygame.image.load(path_path).convert_alpha()
        tile_data = open(data_path, 'r').read().split('\n')

        num_rows = tile_image.get_height() // self.tile_size
        num_cols = tile_image.get_width() // self.tile_size

        tiles = []

        for row in range(num_rows):
            for col in range(num_cols):
                tile_rect = pygame.FRect(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
                tile_surface = tile_image.subsurface(tile_rect)
                tiles.append(tile_surface.copy())

        for i, line in enumerate(tile_data):
            index, name = line.split(':')
            self.tiles[name] = tiles[int(index)]

    def get(self, tile):
        return self.tiles[tile]

    def test(self, tile, display):
        display.blit(self.tiles[tile], (0, 0))
