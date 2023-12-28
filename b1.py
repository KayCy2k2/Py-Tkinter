import tkinter as tk

class MouseCoordinates:
    def __init__(self, window):
        self.window = window
        self.window.config(background='lightblue')
        self.create_widgets()

    def create_widgets(self):
        self.coord_label = tk.Label(self.window, background="lightblue")
        self.coord_label.pack(side=tk.BOTTOM, anchor='e')

        self.window.bind("<Motion>", self.update_mouse_coordinates)

    def update_mouse_coordinates(self, event):
        x, y = event.x, event.y
        self.coord_label.config(text=f"X: {x}, Y: {y}")

    def run(self):
        self.window.mainloop()

window = tk.Tk()
mouse_coordinates = MouseCoordinates(window)
mouse_coordinates.run()
