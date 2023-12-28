import tkinter as tk

class MouseCoordinates:
    def __init__(self, window):
        self.window = window
        self.window.config(background='lightblue')
        self.create_widgets()

        self.start_x = None
        self.start_y = None
        self.rectangle = None

    def create_widgets(self):
        self.canvas = tk.Canvas(self.window, background='lightblue')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.horizontal_line = self.canvas.create_line(0, 0, self.window.winfo_width(), 0, fill='red', width=2)
        self.vertical_line = self.canvas.create_line(0, 0, 0, self.window.winfo_height(), fill='blue', width=2)

        self.coord_label = tk.Label(self.window, background="lightblue")
        self.coord_label.pack(side=tk.BOTTOM, anchor='e')

        self.window.bind("<Motion>", self.update_mouse_coordinates)
        self.window.bind("<Button-1>", self.start_rectangle)
        self.window.bind("<B1-Motion>", self.draw_rectangle)

    def update_mouse_coordinates(self, event):
        x, y = event.x, event.y
        self.coord_label.config(text=f"X: {x}, Y: {y}")
        self.canvas.coords(self.horizontal_line, 0, y, self.window.winfo_width(), y)
        self.canvas.coords(self.vertical_line, x, 0, x, self.window.winfo_height())

    def start_rectangle(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def draw_rectangle(self, event):
        if self.rectangle:
            self.canvas.delete(self.rectangle)
        x = min(self.start_x, event.x)
        y = min(self.start_y, event.y)
        width = abs(self.start_x - event.x)
        height = abs(self.start_y - event.y)
        self.rectangle = self.canvas.create_rectangle(x, y, x + width, y + height, outline='black', width=2)

    def run(self):
        self.window.mainloop()

window = tk.Tk()
mouse_coordinates = MouseCoordinates(window)
mouse_coordinates.run()
