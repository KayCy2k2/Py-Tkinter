import tkinter as tk

class MouseCoordinates:
    def __init__(self, window):
        self.window = window
        self.window.config(background='lightblue')
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.window, background='lightblue')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.horizontal_line = self.canvas.create_line(0, 0, self.window.winfo_width(), 0, fill='red', width=2)
        self.vertical_line = self.canvas.create_line(0, 0, 0, self.window.winfo_height(), fill='blue', width=2)

        self.coord_label = tk.Label(self.window, background="lightblue")
        self.coord_label.pack(side=tk.BOTTOM, anchor='e')

        self.window.bind("<Motion>", self.update_mouse_coordinates)

    def update_mouse_coordinates(self, event):
        x, y = event.x, event.y
        self.coord_label.config(text=f"X: {x}, Y: {y}")
        self.canvas.coords(self.horizontal_line, 0, y, self.window.winfo_width(), y)
        self.canvas.coords(self.vertical_line, x, 0, x, self.window.winfo_height())

    def run(self):
        self.window.mainloop()

window = tk.Tk()
mouse_coordinates = MouseCoordinates(window)
mouse_coordinates.run()
