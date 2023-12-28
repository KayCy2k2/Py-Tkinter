import threading
import tkinter as tk
from googletrans import Translator

class TranslationApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Dịch Tiếng Việt - Tiếng Anh")

        self.create_widgets()

    def create_widgets(self):
        input_frame = tk.Frame(self.window)
        input_frame.pack(pady=10)

        input_label = tk.Label(input_frame, text="Nhập văn bản:")
        input_label.pack(side=tk.LEFT)

        self.input_text = tk.Text(input_frame, height=5)
        self.input_text.pack(side=tk.LEFT)

        clear_input_button = tk.Button(input_frame, text="Xóa", command=self.clear_input)
        clear_input_button.pack(side=tk.LEFT)

        translate_frame = tk.Frame(self.window)
        translate_frame.pack(pady=10)

        translate_button_en = tk.Button(translate_frame, text="Dịch Việt -> Anh", command=self.translate_to_english)
        translate_button_en.pack(side=tk.LEFT)

        translate_button_vi = tk.Button(translate_frame, text="Dịch Anh -> Việt", command=self.translate_to_vietnamese)
        translate_button_vi.pack(side=tk.LEFT)

        output_frame = tk.Frame(self.window)
        output_frame.pack(pady=10)

        output_label = tk.Label(output_frame, text="Kết quả dịch:")
        output_label.pack(side=tk.LEFT)

        self.output_text = tk.Text(output_frame, height=5)
        self.output_text.pack(side=tk.LEFT)

        clear_output_button = tk.Button(output_frame, text="Xóa", command=self.clear_output)
        clear_output_button.pack(side=tk.LEFT)

    def translate_text(self, src, dest):
        text = self.input_text.get(1.0, tk.END).strip()
        translator = Translator(service_urls=['translate.google.com'])
        translated = translator.translate(text, src=src, dest=dest)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, translated.text)

    def clear_input(self):
        self.input_text.delete(1.0, tk.END)

    def clear_output(self):
        self.output_text.delete(1.0, tk.END)

    def translate_to_english(self):
        threading.Thread(target=self.translate_text, args=('vi', 'en')).start()

    def translate_to_vietnamese(self):
        threading.Thread(target=self.translate_text, args=('en', 'vi')).start()

    def run(self):
        self.window.mainloop()
        
app = TranslationApp()
app.run()
