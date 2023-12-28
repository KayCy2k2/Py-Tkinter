import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import threading

class ImageConverter:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Chương trình chuyển đổi ảnh")
        self.window.geometry('450x300')

        self.image_path = ""
        self.converted_image = None
        self.output_format = ".png"
        self.current_photo = None

        self.image_references = {}

        self.menu_bar = tk.Menu(self.window)
        self.window.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Tệp", menu=self.file_menu)
        self.file_menu.add_command(label="Mở ảnh", command=self.open_image)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Thoát", command=self.exit_app)

        self.convert_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Chuyển đổi", menu=self.convert_menu)
        self.convert_menu.add_command(label="Chuyển đổi ảnh", command=self.convert_image)

        self.frame = tk.Frame(self.window)
        self.frame.pack(pady=10)

        self.preview_label = tk.Label(self.frame)
        self.preview_label.pack()

        self.path_label = tk.Label(self.frame, text="")
        self.path_label.pack()

        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack(pady=10)

        self.open_button = tk.Button(self.button_frame, text="Mở ảnh", command=self.open_image)
        self.open_button.pack(side=tk.LEFT, padx=(0, 10))

        self.output_format_variable = tk.StringVar()
        self.output_format_variable.set(".png")

        self.output_format_menu = tk.OptionMenu(self.button_frame, self.output_format_variable,
                                                ".png", ".jpg", ".jpeg", ".ico", ".gif", ".bmp")
        self.output_format_menu.pack(side=tk.LEFT, padx=(0, 10))

        self.convert_button = tk.Button(self.button_frame, text="Chuyển đổi ảnh", command=self.convert_image, state="disabled")
        self.convert_button.pack(side=tk.LEFT)

        self.output_format_variable.trace('w', self.update_output_format)

    def open_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=(("Tệp ảnh", "*.jpg;*.jpeg;*.png"),))
        if self.image_path:
            image = Image.open(self.image_path)
            image = image.resize((200, 200), Image.LANCZOS)
            self.current_photo = ImageTk.PhotoImage(image)
            self.preview_label.configure(image=self.current_photo)
            self.preview_label.image = self.current_photo
            self.convert_button.config(state="normal")
            self.path_label.config(text=self.image_path)
    
    def convert_image(self):
        if self.image_path:
            image = Image.open(self.image_path)
            self.converted_image = image.convert("RGBA")
            save_thread = threading.Thread(target=self.save_image)
            save_thread.start()

    def save_image(self):
        save_path = filedialog.asksaveasfilename(defaultextension=self.output_format,
                                                 filetypes=[("Tất cả các tệp", "*.*")])
        if save_path:
            format = save_path.split(".")[-1].upper()
            try:
                self.converted_image.save(save_path)
                self.window.after(0, self.show_notification, f"Đã lưu ảnh thành công dưới định dạng {format}!")
                self.image_references[save_path] = ImageTk.PhotoImage(self.converted_image)
            except Exception as e:
                self.window.after(0, self.show_notification, "Đã xảy ra lỗi khi lưu ảnh.")

    def show_notification(self, message):
        messagebox.showinfo("Thông báo", message)

    def exit_app(self):
        self.image_references.clear()
        if messagebox.askokcancel("Thoát", "Bạn có chắc chắn muốn thoát không?"):
            self.window.destroy()

    def update_output_format(self, *args):
        self.output_format = self.output_format_variable.get()

    def run(self):
        self.window.mainloop()

ImageConverter().run()
