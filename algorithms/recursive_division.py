import random
from algorithms.base_algorithm import Algorithm
from base.grid3d import Grid3d
from exporters.ascii_exporter import ASCIIExporter


class RecursiveDivision(Algorithm):
    """

    """

    def on(self, grid: Grid3d) -> None:
        self._grid = grid
        for cell in grid.each_cell():
            if cell.north is not None:
                cell += cell.north
            if cell.south is not None:
                cell += cell.south
            if cell.east is not None:
                cell += cell.east
            if cell.west is not None:
                cell += cell.west
            if cell.up is not None:
                cell += cell.up
            if cell.down is not None:
                cell += cell.down
        self.divide(0, 0, 0, 0, grid.levels, grid.rows, grid.columns)
        # ASCIIExporter().render(self._grid)

    def divide(self, loop, level, row, column, depth, height, width):
        print("start", loop, level, row, column, depth, height, width)
        ASCIIExporter().render(self._grid)
        m = max(depth, height, width)
        r = random.random() >= .9
        if height == 1 or width == 1 or depth == 1 or (height <= 5 and width <=5 and depth <=5 and r):
            print("done", loop, level, row, column, depth, height, width)
            return

        if m == depth:
            divide_at = random.randint(level, level+depth-2)
            passage_at = [divide_at, random.randint(row, row+height-1), random.randint(column, column+width-1)]
            for x in range(row, row+height):
                for y in range(column, column+width):
                    if [divide_at, x, y] != passage_at:
                        c = self._grid[divide_at, x, y]
                        c.unlink(c.up)
            self.divide(loop+1, level, row, column, divide_at+1-level, height, width)
            self.divide(loop+1, divide_at+1, row, column, depth+level-divide_at-1, height, width)
        elif m == width:
            divide_at = random.randint(column, column+width-2)
            passage_at = [random.randint(level, level+depth-1), random.randint(row, row+height-1), divide_at]
            for w in range(level, level+depth):
                for x in range(row, row+height):
                    if [w, x, divide_at] != passage_at:
                        c = self._grid[w, x, divide_at]
                        c.unlink(c.east)
            self.divide(loop+1, level, row, column, depth, height, divide_at+1-column)
            self.divide(loop+1, level, row, divide_at+1, depth, height, width+column-divide_at-1)
        elif m == height:
            divide_at = random.randint(row, row+height-2)
            passage_at = [random.randint(level, level+depth-1), divide_at, random.randint(column, column+width-1)]
            for w in range(level, level+depth):
                for y in range(column, column+width):
                    if [w, divide_at, y] != passage_at:
                        c = self._grid[w, divide_at, y]
                        c.unlink(c.south)
            self.divide(loop+1, level, row, column, depth, divide_at+1-row, width)
            self.divide(loop+1, level, divide_at+1, column, depth, height+row-divide_at-1, width)
