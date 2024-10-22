import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import queue
import os
from photo_renamer import rename_photos, load_last_used_folders, save_last_used_folders

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ModernPhotoRenamerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Modern Photo Renamer")
        self.geometry("1000x800")
        
        self.excel_path = tk.StringVar()
        self.photos_dirs = []
        self.output_dir = tk.StringVar()
        
        self.last_used_folders = load_last_used_folders()
        
        self.create_widgets()
        
        self.log_queue = queue.Queue()
        self.after_id = None
        self.start_log_monitor()

    def create_widgets(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Excel file selection
        self.excel_label = ctk.CTkLabel(self, text="Excel File:")
        self.excel_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.excel_entry = ctk.CTkEntry(self, textvariable=self.excel_path, width=400)
        self.excel_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.excel_button = ctk.CTkButton(self, text="Browse", command=self.browse_excel)
        self.excel_button.grid(row=0, column=2, padx=10, pady=10)

        # Photos directories selection
        self.photos_label = ctk.CTkLabel(self, text="Photos Directories:")
        self.photos_label.grid(row=1, column=0, padx=10, pady=10, sticky="ne")
        self.photos_listbox = tk.Listbox(self, width=60, height=5)
        self.photos_listbox.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.photos_scroll = ctk.CTkScrollbar(self, command=self.photos_listbox.yview)
        self.photos_scroll.grid(row=1, column=2, sticky="ns")
        self.photos_listbox.configure(yscrollcommand=self.photos_scroll.set)
        
        self.add_button = ctk.CTkButton(self, text="Add", command=self.add_photos_dir)
        self.add_button.grid(row=1, column=3, padx=10, pady=(10, 5))
        self.remove_button = ctk.CTkButton(self, text="Remove", command=self.remove_photos_dir)
        self.remove_button.grid(row=1, column=3, padx=10, pady=(5, 10), sticky="s")

        # Output directory selection
        self.output_label = ctk.CTkLabel(self, text="Output Directory:")
        self.output_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.output_combo = ctk.CTkComboBox(self, variable=self.output_dir, width=400)
        self.output_combo.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.output_combo.configure(values=self.last_used_folders.get('output_dirs', []))
        self.output_button = ctk.CTkButton(self, text="Browse", command=self.browse_output_dir)
        self.output_button.grid(row=2, column=2, padx=10, pady=10)

        # Rename button and mode switch
        self.rename_button = ctk.CTkButton(self, text="Rename Photos", command=self.start_renaming)
        self.rename_button.grid(row=3, column=1, pady=20, sticky="e", padx=(0, 10))
        self.mode_switch = ctk.CTkSwitch(self, text="Dark Mode", command=self.toggle_mode)
        self.mode_switch.grid(row=3, column=2, pady=20, sticky="w")

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.grid(row=4, column=0, columnspan=3, pady=10, padx=10, sticky="ew")
        self.progress_bar.set(0)

        # Log display
        self.log_display = ctk.CTkTextbox(self, width=600, height=200)
        self.log_display.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Last result summary
        self.last_result_label = ctk.CTkLabel(self, text="Last Result: N/A")
        self.last_result_label.grid(row=6, column=0, columnspan=3, pady=10, sticky="ew")

    def toggle_mode(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")

    def browse_excel(self):
        filename = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if filename:
            self.excel_path.set(filename)
            self.update_last_used_folder('excel_path', filename)

    def add_photos_dir(self):
        dirname = filedialog.askdirectory()
        if dirname and dirname not in self.photos_dirs:
            self.photos_dirs.append(dirname)
            self.photos_listbox.insert(tk.END, dirname)
            self.update_last_used_folder('photos_dirs', dirname)

    def remove_photos_dir(self):
        selection = self.photos_listbox.curselection()
        if selection:
            index = selection[0]
            self.photos_listbox.delete(index)
            del self.photos_dirs[index]

    def browse_output_dir(self):
        dirname = filedialog.askdirectory()
        if dirname:
            self.output_dir.set(dirname)
            self.update_last_used_folder('output_dirs', dirname)

    def update_last_used_folder(self, key, value):
        if key not in self.last_used_folders:
            self.last_used_folders[key] = []
        if value in self.last_used_folders[key]:
            self.last_used_folders[key].remove(value)
        self.last_used_folders[key].insert(0, value)
        self.last_used_folders[key] = self.last_used_folders[key][:5]
        save_last_used_folders(self.last_used_folders)
        if key == 'output_dirs':
            self.output_combo.configure(values=self.last_used_folders[key])

    def start_renaming(self):
        excel_path = self.excel_path.get()
        output_dir = self.output_dir.get()
        
        if not excel_path or not self.photos_dirs or not output_dir:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        self.progress_bar.set(0)
        self.log_display.delete("1.0", tk.END)
        
        threading.Thread(target=self.rename_photos_thread, args=(excel_path, self.photos_dirs, output_dir), daemon=True).start()

    def rename_photos_thread(self, excel_path, photos_dirs, output_dir):
        try:
            total_files = sum(len([f for f in os.listdir(d) if os.path.isfile(os.path.join(d, f))]) for d in photos_dirs)
            processed_files = 0
            
            for photos_dir in photos_dirs:
                rename_photos(excel_path, photos_dir, output_dir, self.log_queue, self.update_progress)
                processed_files += len([f for f in os.listdir(photos_dir) if os.path.isfile(os.path.join(photos_dir, f))])
                self.progress_bar.set(processed_files / total_files)
            
            self.after(0, lambda: self.last_result_label.configure(text="Last Result: Success", text_color="green"))
        except Exception as e:
            self.log_queue.put(f"An error occurred: {str(e)}")
            self.after(0, lambda: self.last_result_label.configure(text="Last Result: Error", text_color="red"))

    def update_progress(self, value):
        self.progress_bar.set(value / 100)

    def start_log_monitor(self):
        self.check_log_queue()

    def check_log_queue(self):
        while not self.log_queue.empty():
            message = self.log_queue.get()
            self.log_display.insert(tk.END, message + '\n')
            self.log_display.see(tk.END)
        self.after_id = self.after(100, self.check_log_queue)

if __name__ == "__main__":
    app = ModernPhotoRenamerGUI()
    app.mainloop()