import tkinter as tk
from tkinter import filedialog, font
import subprocess
import threading
from queue import Queue

class PythonInstallerApp:
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("Python Installer")

        self.create_widgets()
        self.stop_process = False

    def create_widgets(self):
        # Tạo frame chứa các widgets
        frame = tk.Frame(self.master, padx=10, pady=10)
        frame.pack()

        file_label = tk.Label(frame, text="Python file:", fg="blue")  
        file_label.grid(row=0, column=0, sticky=tk.W)
        self.file_entry = tk.Entry(frame, width=100, bg="lightgray") 
        self.file_entry.grid(row=0, column=1)
        file_button = tk.Button(frame, text="Select File", command=self.select_file, fg="black", bg="lightgreen") 
        file_button.grid(row=0, column=2)

        image_label = tk.Label(frame, text="Image file:", fg="blue")
        image_label.grid(row=1, column=0, sticky=tk.W)
        self.image_entry = tk.Entry(frame, width=100, bg="lightgray")
        self.image_entry.grid(row=1, column=1)
        image_button = tk.Button(frame, text="Select Image", command=self.select_image, fg="black", bg="lightgreen")
        image_button.grid(row=1, column=2)

        dir_label = tk.Label(frame, text="Output directory:", fg="blue")
        dir_label.grid(row=2, column=0, sticky=tk.W)
        self.dir_entry = tk.Entry(frame, width=100, bg="lightgray")
        self.dir_entry.grid(row=2, column=1)
        dir_button = tk.Button(frame, text="Select Directory", command=self.select_directory, fg="black", bg="lightgreen")
        dir_button.grid(row=2, column=2)
        
        name_label = tk.Label(frame, text="Name File:", fg="blue")
        name_label.grid(row=3, column=0, sticky=tk.W)
        self.name_entry = tk.Entry(frame, width=30, bg="lightgray")
        self.name_entry.grid(row=3, column=1, sticky=tk.W)
        
        # Tạo frame mới để chứa nút Install và Stop
        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=10)

        self.install_button = tk.Button(button_frame, text="Install", command=self.install_thread, fg="black", bg="orange")
        self.install_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(button_frame, text="Stop", command=self.stop_installation, fg="black", bg="red")
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Tạo khung hiển thị nội dung cài đặt
        display_frame = tk.Frame(self.master, bd=1, relief=tk.SUNKEN)
        display_frame.pack(fill=tk.BOTH, expand=True)

        self.display_text = tk.Text(display_frame, wrap=tk.WORD, bg="white", fg="blue")  # Đặt màu nền đen và chữ màu trắng
        self.display_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(display_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.display_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.display_text.yview)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(tk.END, file_path)

    def select_image(self):
        filetypes = [("All files", "*.*"), ("PNG files", "*.png"), ("ICO files", "*.ico")]
        image_path = filedialog.askopenfilename(filetypes=filetypes)
        self.image_entry.delete(0, tk.END)
        self.image_entry.insert(tk.END, image_path)

    def select_directory(self):
        dir_path = filedialog.askdirectory()
        self.dir_entry.delete(0, tk.END)
        self.dir_entry.insert(tk.END, dir_path)

    def stop_installation(self):
        self.stop_process = True

    def install(self):
        python_file = self.file_entry.get()
        image_file = self.image_entry.get()
        output_dir = self.dir_entry.get()
        name_file = self.name_entry.get()
        self.display_text.delete('1.0', tk.END)

        command = f"pyinstaller --clean -F -w -y -n {name_file} -i {image_file} {python_file}"
        process = subprocess.Popen(command, cwd=output_dir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        # Sử dụng Queue để lưu trữ đầu ra từ quá trình con
        output_queue = Queue()

        def enqueue_output(out, queue):
            for line in iter(out.readline, b''):
                queue.put(line.decode('utf-8').strip())
            out.close()

        # Khởi tạo một luồng mới để lấy đầu ra từ quá trình con và đưa vào hàng đợi
        t = threading.Thread(target=enqueue_output, args=(process.stdout, output_queue))
        t.daemon = True  # Đánh dấu luồng là daemon để nó tự động kết thúc khi chương trình chính kết thúc
        t.start()

        while process.poll() is None:  # Kiểm tra xem quá trình con đã kết thúc hay chưa
            if self.stop_process:  # Kiểm tra xem nút "Dừng" đã được nhấn chưa
                break

            while not output_queue.empty():
                output = output_queue.get()
                self.display_text.insert(tk.END, output + '\n')
                self.display_text.configure(foreground='blue')
                self.display_text.see(tk.END)

        if not self.stop_process:
            self.display_text.insert(tk.END, "Installation complete! ✔️\n")
            self.display_text.configure(fg='green')
            self.display_text.see(tk.END)
        else:
            self.display_text.insert(tk.END, "Installation stopped by user. ❌\n")
            self.display_text.configure(foreground='red')
            self.stop_process = not self.stop_process

        self.install_button.config(state=tk.NORMAL)

    def install_thread(self):
        self.install_button.config(state=tk.DISABLED)
        t = threading.Thread(target=self.install)
        t.start()

    def run(self):
        self.master.mainloop()
        self.stop_process = True  # Đảm bảo rằng quá trình cài đặt sẽ dừng khi cửa sổ chính được đóng

app = PythonInstallerApp()
app.run()
