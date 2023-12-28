import tkinter as tk
import threading
import pydoc
import pkg_resources
import inspect, xlwings

class LibraryDisplayApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Library Display App")
        self.window.geometry("800x500")

        self.frame_library = tk.Frame(self.window)
        self.frame_library.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.listbox_library = tk.Listbox(self.frame_library, bg="lightblue", fg="black")  # Thêm màu nền lightblue và màu chữ black
        self.listbox_library.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.frame_library, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_library.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox_library.yview)

        self.frame_text = tk.Frame(self.window)
        self.frame_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar_text = tk.Scrollbar(self.frame_text)
        self.scrollbar_text.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_box = tk.Text(self.frame_text, yscrollcommand=self.scrollbar_text.set, bg="white", fg="black")  # Thêm màu nền white và màu chữ black
        self.text_box.pack(fill=tk.BOTH, expand=True)

        self.scrollbar_text.config(command=self.text_box.yview)

        self.frame_search = tk.Frame(self.window)
        self.frame_search.pack(pady=10)

        self.label_search = tk.Label(self.frame_search, text="Tìm kiếm:", fg="black")  # Thêm màu chữ black
        self.label_search.pack(side=tk.LEFT)

        self.entry_search = tk.Entry(self.frame_search)
        self.entry_search.pack(side=tk.LEFT)

        self.btn_search = tk.Button(self.frame_search, text="Tìm kiếm", command=self.search_library, bg="lightgreen", fg="black")  # Thêm màu nền lightgreen và màu chữ black
        self.btn_search.pack(side=tk.LEFT)

        self.listbox_library.bind('<<ListboxSelect>>', self.display_library_content)

        self.display_installed_libraries()

    def display_library_content(self, event):
        selected_indices = self.listbox_library.curselection()
        
        if selected_indices:
            first_index = selected_indices[0]
            selected_library = self.listbox_library.get(first_index)
            
            self.text_box.delete("1.0", tk.END)
            
            def get_library_info():
                try:
                    module = __import__(selected_library)
                    doc = pydoc.plain(pydoc.render_doc(module))

                    self.text_box.insert(tk.END, doc)
                except ImportError:
                    error_msg = f"Không tìm thấy module: {selected_library}"
                    self.text_box.insert(tk.END, error_msg)
                except xlwings.XlwingsError:
                    error_msg = f"Lỗi: Không tìm thấy ứng dụng Excel hoạt động"
                    self.text_box.insert(tk.END, error_msg)
            
            search_thread = threading.Thread(target=get_library_info)
            search_thread.start()

    def display_installed_libraries(self, search_query=None):
        installed_packages = pkg_resources.working_set
        self.listbox_library.delete(0, tk.END)

        for package in installed_packages:
            library_name = package.key

            if not search_query or search_query.lower() in library_name.lower():
                self.listbox_library.insert(tk.END, library_name)

    def search_library(self):
        query = self.entry_search.get()
        self.display_installed_libraries(query)

    def run(self):
        self.window.mainloop()

app = LibraryDisplayApp()
app.run()
