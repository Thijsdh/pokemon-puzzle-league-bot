from typing import List, Union
from cell import Cell
from cell_change import CellChange


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.cells = []
        self.filled_cell_count = 0

        for y in range(self.height):
            for x in range(self.width):
                self.cells.append(Cell(x, y))

    def clone(self):
        g = Grid(self.width, self.height)
        for cell in self.cells:
            g.set_cell_id(cell.x, cell.y, cell.id)
        return g

    def get_cell_ids(self) -> List[int]:
        return [cell.id for cell in self.cells]

    def get_score(self) -> int:
        return self.filled_cell_count

    def get_cell(self, x: int, y: int) -> Cell:
        return self.cells[x + y * self.width]

    def set_cell_id(self, x: int, y: int, id: Union[str, None]) -> None:
        cell = self.get_cell(x, y)
        if cell.id is None:
            self.filled_cell_count += 1
        if id is None:
            self.filled_cell_count -= 1
        cell.id = id

    def exec_gravity(self, cell: Cell) -> List[CellChange]:
        # If the cell under cell is empty, the cell under cell becomes the cell.
        newY = cell.y
        while newY - 1 >= 0 and self.get_cell(cell.x, newY - 1).id is None:
            newY -= 1

        changes = []
        if newY != cell.y:
            id = cell.id
            self.set_cell_id(cell.x, newY, cell.id)
            self.set_cell_id(cell.x, cell.y, None)
            changes = [
                CellChange(cell.x, newY, None, id, 'gravity'),
                CellChange(cell.x, cell.y, id, None, 'gravity'),
            ]

        return changes

    def exec_neighbours(self, cell: Cell) -> List[CellChange]:
        changes: List[CellChange] = []

        # Find horizontal neighbours
        row = [cell]
        x = cell.x
        while x - 1 >= 0 and self.get_cell(x - 1, cell.y).id == cell.id:
            row.append(self.get_cell(x - 1, cell.y))
            x -= 1
        x = cell.x
        while x + 1 < self.width and self.get_cell(x + 1, cell.y).id == cell.id:
            row.append(self.get_cell(x + 1, cell.y))
            x += 1

        if len(row) >= 3:
            for cell in row:
                changes.append(CellChange(
                    cell.x, cell.y, cell.id, None, 'neighbours_h'))
                self.set_cell_id(cell.x, cell.y, None)

        # Find vertical neighbours
        col = [cell]
        y = cell.y
        while y - 1 >= 0 and self.get_cell(cell.x, y - 1).id == cell.id:
            col.append(self.get_cell(cell.x, y - 1))
            y -= 1
        y = cell.y
        while y + 1 < self.height and self.get_cell(cell.x, y + 1).id == cell.id:
            col.append(self.get_cell(cell.x, y + 1))
            y += 1

        if len(col) >= 3:
            for cell in col:
                changes.append(CellChange(
                    cell.x, cell.y, cell.id, None, 'neighbours_v'))
                self.set_cell_id(cell.x, cell.y, None)

        return changes

    def exec_game_rules_all(self) -> List[CellChange]:
        before = []
        changes: List[CellChange] = []

        while self.get_cell_ids() != before:
            before = self.get_cell_ids()

            for cell in [cell for cell in self.cells]:
                if cell.id is not None:
                    changes += self.exec_gravity(cell)

            for cell in [cell for cell in self.cells]:
                if cell.id is not None:
                    changes += self.exec_neighbours(cell)

        return changes

    def swap(self, x: int, y: int) -> List[CellChange]:
        cell1 = self.get_cell(x, y)
        cell2 = self.get_cell(x + 1, y)

        if cell1.id == cell2.id:
            return []

        tmp = cell1.id
        cell1.id = cell2.id
        cell2.id = tmp

        return [
            CellChange(x, y, cell2.id, cell1.id, 'swap'),
            CellChange(x + 1, y, cell1.id, cell2.id, 'swap')
        ]

    def rollback(self, changes: List[CellChange]) -> None:
        for change in reversed(changes):
            self.get_cell(change.x, change.y).id = change.from_id

    def print(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                cell = self.get_cell(x, self.height - 1 - y)
                if cell.id is not None:
                    print(cell.id[0], end=" ")
                else:
                    print(" ", end=" ")
            print()

        print()
