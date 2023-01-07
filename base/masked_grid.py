from typing import Generator, List, Optional
from base.cell import Cell, CellList
from base.grid3d import Cell3d, Grid3d
from base.distance_grid import DistanceGrid
from base.mask import Mask


class MaskedGrid(Grid3d):
    @property
    def mask(self) -> int:
        return self._mask

    def __init__(self, mask: Mask) -> None:
        self._mask: Mask = mask
        super().__init__(mask.levels, mask.rows, mask.columns)

    def prepare_grid(self) -> List[List[List[Cell3d]]]:
        return [[[Cell3d(level, row, column) if self._mask[level, row, column] is True else None for column in range(self.columns)] for row in range(self.rows)] for level in range(self.levels)]

    def each_cell_in_row(self, row) -> Generator[CellList, None, None]:
        for cell in row:
            yield cell if cell is not None else Cell3d(-1, -1, -1)

    def random_cell(self) -> Cell:
        return self.cell_at(*self._mask.random_cell())

    def size(self) -> int:
        return self._mask.count()
