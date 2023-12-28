import tkinter as tk

class ColorViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Color Viewer")
        self.configure(width=500, height=300)
        self.resizable(False, False)

        self.slider_frame = tk.Frame(self)
        self.slider_frame.pack(side=tk.RIGHT)

        self.red_slider = tk.Scale(self.slider_frame, from_=0, to=255, orient=tk.HORIZONTAL,
                                   label="Red", command=self.update_color, resolution=1, tickinterval=50, length=400)
        self.green_slider = tk.Scale(self.slider_frame, from_=0, to=255, orient=tk.HORIZONTAL,
                                     label="Green", command=self.update_color, resolution=1, tickinterval=50, length=400)
        self.blue_slider = tk.Scale(self.slider_frame, from_=0, to=255, orient=tk.HORIZONTAL,
                                    label="Blue", command=self.update_color, resolution=1, tickinterval=50, length=400)

        self.red_slider.bind("<Button-1>", self.move_slider)
        self.green_slider.bind("<Button-1>", self.move_slider)
        self.blue_slider.bind("<Button-1>", self.move_slider)

        self.red_slider.pack()
        self.green_slider.pack()
        self.blue_slider.pack()

        self.color_frame = tk.Frame(self, width=200, height=200, bg="#000000")
        self.color_frame.pack(padx=10, pady=10)

        self.hex_label = tk.Label(self, text="Hex: #000000")
        self.hex_label.pack()

        self.rgb_label = tk.Label(self, text="RGB: 0, 0, 0")
        self.rgb_label.pack()

    def update_color(self, event=None):
        r = self.red_slider.get()
        g = self.green_slider.get()
        b = self.blue_slider.get()
        
        rgb_text = f'RGB: {r}, {g}, {b}'
        hex_color = f'#{r:02x}{g:02x}{b:02x}'

        self.color_frame.configure(bg=hex_color)
        self.rgb_label.configure(text=rgb_text)
        self.hex_label.configure(text=f'Hex: {hex_color}')

    def move_slider(self, event):
        x = event.x
        y = event.y
        nearest_slider = event.widget
        value = int(nearest_slider.cget("from") + (x / nearest_slider.winfo_width()) * (nearest_slider.cget("to") - nearest_slider.cget("from")))
        nearest_slider.set(value)

    def run(self):
        self.mainloop()
app = ColorViewer()
app.mainloop()
