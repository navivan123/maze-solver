from window import Window

from draw import Point, Line, Cell, Maze


def main():
    num_rows = 29
    num_cols = 18
    margin = 50
    screen_x = 1600
    screen_y = 1200
    cell_size_x = 50 #(screen_x - 2 * margin) / num_cols
    cell_size_y = 50 #(screen_y - 2 * margin) / num_rows
    win = Window(screen_x, screen_y)

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win)

    print(maze.solve())

    win.wait_for_close()

main()
