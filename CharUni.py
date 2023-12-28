import tkinter as tk
from tkinter import ttk
import threading

class UnicodeViewerApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Unicode Characters Viewer")
        
        self.menu_var = tk.StringVar(value="ASCII")
        self.chunk_size = 1000

        self.create_widgets()
        self.load_characters(0x0020, 0x007F)
    
    def create_widgets(self):
        self.create_menu()
        self.create_treeview()
        self.create_unicode_text()
        self.create_scrollbar()
        self.create_total_chars_frame()
        self.create_search_frame()

    def create_menu(self):
        self.menu_bar = tk.Menu(self.window)
        self.window.config(menu=self.menu_bar)

        self.character_menu = tk.Menu(self.menu_bar, tearoff=0)
        character_options = [
            ("ASCII", "ASCII"),
            ("Latin-1", "Latin-1"),
            ("Extended Latin", "Extended_Latin"),
            ("Greek", "Greek"),
            ("Cyrillic", "Cyrillic"),
            ("Arabic", "Arabic"),
            ("Devanagari", "Devanagari"),
            ("CJK Unified Ideographs", "CJK_Unified_Ideographs"),
            ("Emoticons", "Emoticons"),
            ("Dingbats", "Dingbats"),
            ("Box Drawing", "Box_Drawing"),
            ("Mathematical Symbols", "Mathematical_Symbols"),
            ("Currency Symbols", "Currency_Symbols"),
            ("Miscellaneous Symbols", "Miscellaneous_Symbols")
        ]
        
        for label, value in character_options:
            self.character_menu.add_radiobutton(
                label=label, variable=self.menu_var, value=value, command=self.menu_selected
            )
        
        self.menu_bar.add_cascade(label="Choose Character Set", menu=self.character_menu)
    
    def create_treeview(self):
        columns = ("Character", "Unicode Code")
        self.characters_tree = ttk.Treeview(self.window, columns=columns, show="headings", height=20)
        self.characters_tree.heading("Character", text="Character")
        self.characters_tree.heading("Unicode Code", text="Unicode Code")
        self.characters_tree.column("Character", width=50, anchor="center")
        self.characters_tree.column("Unicode Code", width=100, anchor="center")
        self.characters_tree.pack(fill=tk.BOTH, expand=True)
        self.characters_tree.bind("<<TreeviewSelect>>", self.character_clicked)
    
    def create_unicode_text(self):
        self.unicode_text = tk.Text(
            self.window, font=("Arial", 10), wrap=tk.WORD, state=tk.DISABLED, height=3, width=40
        )
        self.unicode_text.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.unicode_text.tag_configure("info", foreground="blue")
    
    def create_scrollbar(self):
        scrollbar = ttk.Scrollbar(self.characters_tree, orient=tk.VERTICAL, command=self.characters_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.characters_tree.config(yscrollcommand=scrollbar.set)
    
    def create_total_chars_frame(self):
        total_chars_frame = tk.Frame(self.window)
        total_chars_frame.pack(fill=tk.X, padx=10, pady=5)
        total_chars_label = tk.Label(total_chars_frame, text="Total characters:")
        total_chars_label.pack(side=tk.LEFT)
        self.total_chars_value = tk.Label(total_chars_frame, text="0")
        self.total_chars_value.pack(side=tk.LEFT)
    
    def create_search_frame(self):
        search_frame = tk.Frame(self.window)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        search_label = tk.Label(search_frame, text="Search:")
        search_label.pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        search_button = tk.Button(search_frame, text="Search", command=self.search_characters)
        search_button.pack(side=tk.LEFT)
    
    def load_characters(self, start, end):
        threading.Thread(target=self.populate_characters_tree, args=(start, end)).start()
    
    def populate_characters_tree(self, start, end):
        self.characters_tree.delete(*self.characters_tree.get_children())
        total_chars = 0
        for chunk_start in range(start, end, self.chunk_size):
            chunk_end = min(chunk_start + self.chunk_size, end)
            chunk_chars = [chr(code_point) for code_point in range(chunk_start, chunk_end)]
            for char, code_point in zip(chunk_chars, range(chunk_start, chunk_end)):
                self.characters_tree.insert("", "end", values=[char, f"{code_point:04X}"])
                total_chars += 1
        self.total_chars_value.config(text=str(total_chars))
    
    def character_clicked(self, event):
        selected_item = self.characters_tree.selection()
        if selected_item:
            selected_char = self.characters_tree.item(selected_item[0], "values")[0]
            unicode_value = int(self.characters_tree.item(selected_item[0], "values")[1], 16)
            self.update_unicode_text(selected_char, unicode_value)
    
    def update_unicode_text(self, selected_char, unicode_value):
        self.unicode_text.config(state=tk.NORMAL)
        self.unicode_text.delete(1.0, tk.END)
        self.unicode_text.insert(
            tk.END, f"Character: {selected_char}        Unicode Code: U+{unicode_value:04X}", "info"
        )
        self.unicode_text.config(state=tk.DISABLED)
    
    def menu_selected(self):
        selected_value = self.menu_var.get()
        character_sets = {
            "ASCII": (0x0020, 0x007F),
            "Latin-1": (0x00A0, 0x00FF),
            "Extended_Latin": (0x0100, 0x024F),
            "Greek": (0x0370, 0x03FF),
            "Cyrillic": (0x0400, 0x04FF),
            "Arabic": (0x0600, 0x06FF),
            "Devanagari": (0x0900, 0x097F),
            "CJK_Unified_Ideographs": (0x4E00, 0x9FFF),
            "Emoticons": (0x1F600, 0x1F64F),
            "Dingbats": (0x2700, 0x27BF),
            "Box_Drawing": (0x2500, 0x257F),
            "Mathematical_Symbols": (0x2200, 0x22FF),
            "Currency_Symbols": (0x20A0, 0x20CF),
            "Miscellaneous_Symbols": (0x2600, 0x26FF)
        }
        
        start, end = character_sets.get(selected_value, (0, 0))
        self.load_characters(start, end)

    def search_characters(self):
        query = self.search_entry.get().lower()
        for item in self.characters_tree.get_children():
            char = self.characters_tree.item(item, "values")[0]
            if query in char.lower():
                self.characters_tree.selection_set(item)
                self.characters_tree.see(item)
                return

    def run(self):
        self.window.mainloop()

app = UnicodeViewerApp()
app.run()
