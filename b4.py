import tkinter as tk

class MouseCoordinates:
    def __init__(self, window):
        self.window = window
        self.window.config(background='lightblue')
        self.create_widgets()

        self.is_drawing = False
        self.start_x = 0
        self.start_y = 0

    def create_widgets(self):
        self.canvas = tk.Canvas(self.window, background='lightblue')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.horizontal_line = self.canvas.create_line(0, 0, self.window.winfo_width(), 0, fill='red', width=2)
        self.vertical_line = self.canvas.create_line(0, 0, 0, self.window.winfo_height(), fill='blue', width=2)

        self.coord_label = tk.Label(self.window, background="lightblue")
        self.coord_label.pack(side=tk.BOTTOM, anchor='e')

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw_line)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        self.window.bind("<Motion>", self.update_mouse_coordinates)

    def start_drawing(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.is_drawing = True

    def draw_line(self, event):
        if self.is_drawing:
            x, y = event.x, event.y
            self.canvas.coords(self.horizontal_line, 0, y, self.window.winfo_width(), y)
            self.canvas.coords(self.vertical_line, x, 0, x, self.window.winfo_height())

    def stop_drawing(self, event):
        self.is_drawing = False

    def update_mouse_coordinates(self, event):
        x, y = event.x, event.y
        self.coord_label.config(text=f"X: {x}, Y: {y}")

    def run(self):
        self.window.mainloop()

window = tk.Tk()
mouse_coordinates = MouseCoordinates(window)
mouse_coordinates.run()
