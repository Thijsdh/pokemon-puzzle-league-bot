from typing import Union


class Cell:
    def __init__(self, x: int, y: int, id: Union[str, None] = None):
        self.x = x
        self.y = y
        self.id = id

    def __str__(self):
        return f"Cell({self.x}, {self.y}, {self.id})"
