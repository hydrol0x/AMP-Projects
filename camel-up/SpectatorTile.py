class SpectatorTile:
    def __init__(self, position, value):
        self.position: int = position
        self.value: bool = value

    def flip_tile(self):
        self.value = not self.value

    def tile_position(self):
        return self.position

    def tile_value(self):
        return self.value

    def set_position(self, new_pos: int):
        self.position = new_pos
