import tkinter as tk

class NewTab:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tab ghi chú")

        self.note_frame = tk.Frame(self.window)
        self.note_frame.pack()

        self.newtab()

    def newtab(self):
        # Create a Scrollbar frame for the Text widget
        scrollbar = tk.Scrollbar(self.note_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a Text widget for note taking
        self.text_area = tk.Text(
            self.note_frame, font=("Arial", 13), yscrollcommand=scrollbar.set
        )
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH)

        # Connect the Scrollbar to the Text widget
        scrollbar.config(command=self.text_area.yview)

        # Add default content to the Text widget (if desired)
        default_note = "Viết ghi chú ở đây..."
        self.text_area.insert(tk.END, default_note)

        # Remove default text when user starts typing
        def clear_default_text(event):
            if self.text_area.get(1.0, "end-1c") == default_note:
                self.text_area.delete(1.0, tk.END)

        # Show default text if no characters are entered
        def show_default_text(event):
            if not self.text_area.get(1.0, "end-1c"):
                self.text_area.insert(tk.END, default_note)

        # Bind event handling functions to the Text widget
        self.text_area.bind("<KeyPress>", clear_default_text)
        self.text_area.bind("<FocusOut>", show_default_text)

    def run(self):
        self.window.mainloop()


app = NewTab()
app.run()
