from typing import Union


class CellChange:
    def __init__(self, x, y, from_id: Union[str, None], to_id: Union[str, None], reason: Union[str, None]):
        self.x = x
        self.y = y
        self.from_id = from_id
        self.to_id = to_id
        self.reason = reason
