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
        ASCIIExporter().render(self._grid)

    def divide(self, loop, level, row, column, depth, height, width):
        print("start", loop, level, row, column, depth, height, width)
        ASCIIExporter().render(self._grid)
        m = max(depth, height, width)
        r = random.random() >= .1
        print(r)
        if height == 1 or width == 1 or (height <= 5 and width <=5 and r):
            print("done", loop, level, row, column, depth, height, width)
            return
        if m == width:
            print("horiz", column, width)
            divide_at = random.randint(column, column+width-2)
            print("WDA", divide_at)
            passage_at = random.randint(row, row+height-1)
            print("WPA", passage_at)
            for x in range(row, row+height):
                print("WC", depth-1, x, divide_at)
                if x != passage_at:
                    c = self._grid[depth-1, x, divide_at]
                    c.unlink(c.east)
            print("westside", loop+1, level, row, column, depth, height, divide_at+1-column)
            self.divide(loop+1, level, row, column, depth, height, divide_at+1-column)
            print("eastside", loop+1, level, row, divide_at+1, depth, height, width+column-divide_at-1)
            self.divide(loop+1, level, row, divide_at+1, depth, height, width+column-divide_at-1)
        elif m == height:
            print("vert", row, height)
            divide_at = random.randint(row, row+height-2)
            print("HDA", divide_at)
            passage_at = random.randint(column, column+width-1)
            print("HPA", passage_at)
            for x in range(column, column+width):
                print("HC", depth-1, x, divide_at)
                if x != passage_at:
                    c = self._grid[depth-1, divide_at, x]
                    c.unlink(c.south)
            print("northside", loop+1, level, row, column, depth, divide_at+1-row, width)
            self.divide(loop+1, level, row, column, depth, divide_at+1-row, width)
            print("southside", loop+1, level, divide_at+1, column, depth, height+row-divide_at-1, width)
            self.divide(loop+1, level, divide_at+1, column, depth, height+row-divide_at-1, width)
        # if m == depth:
        #     divide_at = random.randint(depth)
        #     self.divide(level, row, column, divide_at, height, width)
        #     self.divide(divide_at, row, column, depth-divide_at, height, width)
