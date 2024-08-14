from tkinter import Tk, BOTH, Canvas

class Window:
    
    def __init__(self, width, height):
        self.__root_wdgt = Tk()
        self.__root_wdgt.title("Maze Solver!")
        
        self.__canvas_wdgt = Canvas(self.__root_wdgt, bg="white", height=height, width=width)

        self.__canvas_wdgt.pack(fill=BOTH, expand=1)

        self.__is_window_running = False

        self.__root_wdgt.protocol("WM_DELETE_WINDOW", self.close)

    
    def redraw(self):
        self.__root_wdgt.update_idletasks()
        self.__root_wdgt.update()

    
    def wait_for_close(self):
        self.__is_window_running = True

        while self.__is_window_running:
            self.redraw()
        
        print("Wow, the window closed!")


    def close(self):
        self.__is_window_running = False

    
    def draw_line(self, line, color="black"):
        line.draw(self.__canvas_wdgt, color)
