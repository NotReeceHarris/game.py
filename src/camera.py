class Camera:
    def __init__(self, window):
        self.width = window.get_width()
        self.height = window.get_height()
        self.offset_x = self.width // 2
        self.offset_y = self.height // 2

    def set_window(self, camera):
        self.width = camera.get_width()
        self.height = camera.get_height()
        
    def set_offset(self, x, y):
        self.offset_x = x
        self.offset_y = y