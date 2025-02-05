import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class FileShareGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure File Share")

        self.device_frame = ttk.LabelFrame(root, text="Available Devices")
        self.device_list = tk.Listbox(self.device_frame, height=10)
        self.device_list.pack(padx=10, pady=10)
        self.device_frame.pack(padx=10, pady=5, fill=tk.BOTH)

        self.file_frame = ttk.Frame(root)
        self.file_btn = ttk.Button(self.file_frame, text="Select File", command=self.select_file)
        self.file_label = ttk.Label(self.file_frame, text="No file selected")
        self.file_btn.pack(side=tk.LEFT, padx=5)
        self.file_label.pack(side=tk.LEFT)
        self.file_frame.pack(pady=5)
        
        self.progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, mode='determinate')
        self.progress.pack(fill=tk.X, padx=10, pady=5)
        
        self.logs = tk.Text(root, height=10, state=tk.DISABLED)
        self.logs.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)
        
        self.start_network()
    
    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_label.config(text=file_path.split('/')[-1])
    
    def update_device_list(self, devices):
        self.device_list.delete(0, tk.END)
        for device in devices:
            self.device_list.insert(tk.END, f"{device['name']} ({device['ip']})")
    
    def log_message(self, message):
        self.logs.config(state=tk.NORMAL)
        self.logs.insert(tk.END, message + "\n")
        self.logs.config(state=tk.DISABLED)
    
    def start_network(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = FileShareGUI(root)
    root.mainloop()