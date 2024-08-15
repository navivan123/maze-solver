import time
import random

class Point:
   
    def __init__(self, x, y):
        self.x = x
        self.y = y
#
#
#
class Line:

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, color):
        canvas.create_line( 
                            self.p1.x,
                            self.p1.y,
                            self.p2.x,
                            self.p2.y,
                            fill=color,
                            width=2
                          )
#
#
#
class Cell:
    def __init__(self, win):
        self.has_l_wall = True
        self.has_r_wall = True
        self.has_t_wall = True
        self.has_b_wall = True

        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None

        self.visited = False

        self._win = win


    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2


        line = Line(Point(x1, y1), Point(x1, y2))
        if self.has_l_wall:
            self._win.draw_line(line)
        else:
            self._win.draw_line(line, "white")
            

        line = Line(Point(x2, y1), Point(x2, y2))
        if self.has_r_wall:
            self._win.draw_line(line)
        else:
            self._win.draw_line(line, "white")

        line = Line(Point(x1, y1), Point(x2, y1))
        if self.has_t_wall:
            self._win.draw_line(line)
        else:
            self._win.draw_line(line, "white")
        
        line = Line(Point(x1, y2), Point(x2, y2))
        if self.has_b_wall:
            self._win.draw_line(line)
        else:
            self._win.draw_line(line, "white")


    def draw_move(self, to_cell, undo=False):
        if undo:
            color = "gray"
        else:
            color = "red"

        line = Line(Point(abs(self._x1 + self._x2) // 2, abs(self._y1 + self._y2) // 2), Point(abs(to_cell._x1 + to_cell._x2) // 2, abs(to_cell._y1 + to_cell._y2) // 2))

        self._win.draw_line(line, color)
#
#
#
class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        if seed is not None:
            random.seed(seed)

        self._win = win
        
        self._x1 = x1
        self._y1 = y1

        self._num_rows = num_rows
        self._num_cols = num_cols

        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y

        self._cells = []

        self._create_cells()

        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        
        self._reset_cells_visited()



    def _create_cells(self):
        self._cells = [[Cell(self._win) for i in range(self._num_rows)] for j in range(self._num_cols)]

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)


    def _draw_cell(self, i, j):
        if self._win is None:
            return
        pos_x = self._x1 + j * self._cell_size_x
        pos_y = self._y1 + i * self._cell_size_y

        pos_x2 = pos_x + self._cell_size_x
        pos_y2 = pos_y + self._cell_size_y

        self._cells[i][j].draw(pos_x, pos_y, pos_x2, pos_y2)

        self._animate()

    
    def _animate(self):
        if self._win is None:
            return

        self._win.redraw()
        time.sleep(0.035)


    def _break_entrance_and_exit(self):
        self._cells[0][0].has_l_wall = False
        self._draw_cell(0, 0)

        self._cells[-1][-1].has_r_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True

        while True:
            to_visit = []

            if i < (self._num_cols - 1) and self._cells[i + 1][j].visited == False:
                to_visit.append((i + 1, j))
            
            if j < (self._num_rows - 1) and self._cells[i][j + 1].visited == False:
                to_visit.append((i, j + 1))

            if i > 0 and self._cells[i - 1][j].visited == False:
                to_visit.append((i - 1, j))
            
            if j > 0 and self._cells[i][j - 1].visited == False:
                to_visit.append((i, j - 1))

            if not to_visit:
                
                self._draw_cell(i, j)
                return

            idx = random.randint(0, len(to_visit) - 1)
            
            if to_visit[idx][1] == (j + 1):
                self._cells[i][j].has_r_wall = False
                self._cells[i][j + 1].has_l_wall = False
            
            elif to_visit[idx][0] == (i + 1):
                self._cells[i][j].has_b_wall = False
                self._cells[i + 1][j].has_t_wall = False

            elif to_visit[idx][1] == (j - 1):
                self._cells[i][j].has_l_wall = False
                self._cells[i][j - 1].has_r_wall = False

            elif to_visit[idx][0] == (i - 1):
                self._cells[i][j].has_t_wall = False
                self._cells[i - 1][j].has_b_wall = False
            
            self._break_walls_r(to_visit[idx][0], to_visit[idx][1])


    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False


    def solve(self):
        return self._solve_r(0,0)


    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True

        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        if (i < self._num_cols - 1) and self._cells[i + 1][j].visited == False and self._cells[i][j].has_b_wall == False:
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            is_alive = self._solve_r(i + 1, j)
            if is_alive:
                return True
            self._cells[i][j].draw_move(self._cells[i + 1][j], True)

        if (j < self._num_rows - 1) and self._cells[i][j + 1].visited == False and self._cells[i][j].has_r_wall == False:
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            is_alive = self._solve_r(i, j + 1)
            if is_alive:
                return True
            self._cells[i][j].draw_move(self._cells[i][j + 1], True)

        if i > 0 and self._cells[i - 1][j].visited == False and self._cells[i][j].has_t_wall == False:
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            is_alive = self._solve_r(i - 1, j)
            if is_alive:
                return True
            self._cells[i][j].draw_move(self._cells[i - 1][j], True)

        if j > 0 and self._cells[i][j - 1].visited == False and self._cells[i][j].has_l_wall == False:
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            is_alive = self._solve_r(i, j - 1)
            if is_alive:
                return True
            self._cells[i][j].draw_move(self._cells[i][j - 1], True)

        return False
