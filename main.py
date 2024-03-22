import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import os
import platform
import requests
from PIL import Image, ImageTk

class MEOWCompressorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MEOW File Compressor/Decompressor")

        # Variables for the folders to show up in the list on the GUI
        self.selected_folders = []
        self.compression_level = tk.StringVar(self, "Normal")
        self.compression_method = tk.StringVar(self, "ZIP_DEFLATED")

        # Menubar (pretty much explains itself)
        menubar = tk.Menu(self)

        # File menu also does what the menubar explains at
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Select Folders", command=self.select_folders)
        file_menu.add_command(label="Compress into .MEOW", command=self.compress_folders)
        file_menu.add_command(label="Decompress .MEOW File", command=self.decompress_meow)
        menubar.add_cascade(label="File", menu=file_menu)

        # Settings menu for all of the cool compression
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_radiobutton(label="Fastest", value="fastest", variable=self.compression_level)
        settings_menu.add_radiobutton(label="Faster", value="faster", variable=self.compression_level)
        settings_menu.add_radiobutton(label="Normal", value="normal", variable=self.compression_level)
        settings_menu.add_radiobutton(label="Better", value="better", variable=self.compression_level)
        settings_menu.add_radiobutton(label="Best", value="best", variable=self.compression_level)
        settings_menu.add_separator()
        settings_menu.add_radiobutton(label="ZIP_STORED", value="ZIP_STORED", variable=self.compression_method)
        settings_menu.add_radiobutton(label="ZIP_DEFLATED", value="ZIP_DEFLATED", variable=self.compression_method)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        # About MEOW :)
        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="About MEOW", command=self.show_about_info)
        about_menu.add_command(label="Check for Updates", command=self.check_for_updates)
        menubar.add_cascade(label="About", menu=about_menu)

        self.config(menu=menubar)

        # Toolbar, is it the top thing or the bottom thing? Who knows.
        toolbar = tk.Frame(self)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Another one of the drop down menus.
        file_dropdown = tk.Menu(toolbar, tearoff=0)
        file_dropdown.add_command(label="Select Folders", command=self.select_folders)
        file_dropdown.add_command(label="Compress into .MEOW", command=self.compress_folders)
        file_dropdown.add_command(label="Decompress .MEOW File", command=self.decompress_meow)


        # The "Fancy" Logo starring catcrumb's artwork
        self.logo_image = Image.open("logo.png")  # Load the logo image
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(self, image=self.logo_photo)
        self.logo_label.pack(side=tk.TOP)

        # File Structure‽ Yikes!
        self.listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind("<Double-1>", self.on_listbox_double_click)

        # The thing that tells you what's going on
        self.status_bar = tk.Label(self, text="Waiting...")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def select_folders(self):
        while True:
            folder_path = filedialog.askdirectory(title="Select Folders")
            if folder_path:
                self.selected_folders.append(folder_path)
                self.update_listbox()
            else:
                break

    def on_listbox_double_click(self, event):
        selected_item = self.listbox.curselection()
        if selected_item:
            folder_path = self.selected_folders[selected_item[0]]
            if folder_path in self.selected_folders:
                self.selected_folders.remove(folder_path)
            else:
                self.selected_folders.append(folder_path)
            self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for folder_path in self.selected_folders:
            self.listbox.insert(tk.END, folder_path)

    def compress_folders(self):
        if not self.selected_folders:
            messagebox.showwarning("Warning", "No folders selected.")
            return
        zip_filename = "compressed.meow"
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for folder_path in self.selected_folders:
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, os.path.dirname(folder_path))
                        zipf.write(file_path, arcname=arcname)
                        self.status_bar.config(text=f"Compressing {arcname} into a pie.")
                        self.update()
        self.status_bar.config(text="Compression completed.")
        self.selected_folders = []
        self.update_listbox()

    def decompress_meow(self):
        meow_file = filedialog.askopenfilename(title="Select .meow File to Decompress", filetypes=[("MEOW files", "*.meow")])
        if meow_file:
            with zipfile.ZipFile(meow_file, 'r') as zipf:
                extract_path = filedialog.askdirectory(title="Select Extraction Directory")
                if extract_path:
                    zipf.extractall(path=extract_path)
                    self.status_bar.config(text=f"Decompressing... {meow_file}")
                    self.update()
                    self.status_bar.config(text="Decompression completed.")

    def show_about_info(self):
        about_window = tk.Toplevel(self)
        about_window.title("About MEOW")
        
        # detects your computer and displays it for fun and if you have issues
        os_info = platform.system()
        if os_info == "Windows":
            os_version = platform.win32_ver()
            os_info += f" {os_version[0]}"
        elif os_info == "Darwin":  # macOS
            os_version = platform.mac_ver()
            os_info += f" {os_version[0]}"
        elif os_info == "Linux":
            os_info += f" {platform.dist()[0]} {platform.dist()[1]}"
        else:
            os_info += " (Unknown, probably some rad OS I've never heard of before.)"

        about_label = tk.Label(about_window, text=f"MEOW Version: 1.0\nOperating System: {os_info}\nSupport Email: support@skylarclark.xyz\nI suggest that you make a issue on the Github page.")
        about_label.pack()
        logo_label = tk.Label(about_window, image=self.logo_photo)
        logo_label.pack()

    def check_for_updates(self):
        # Gets the latest version's number and compares it to this
        repo_url = "https://api.github.com/repos/6306/MEOW/releases/latest"
        response = requests.get(repo_url)
        if response.status_code == 200:
            latest_version = response.json()["tag_name"]
            current_version = "1.0"  # current version that you're running
            if latest_version > current_version:
                # """""forces""""" the user to update (could bring new features or bug fixes that people requested in issues on github)
                response = messagebox.askquestion("New Update Available", "New update available. Would you like to download it?")
                if response == "yes":
                    # downloads the update to the current folder that it is in right now
                    download_url = response.json()["assets"][0]["browser_download_url"]
                    download_path = os.path.join(os.getcwd(), "MEOW_Update.zip")
                    with open(download_path, "wb") as f:
                        f.write(requests.get(download_url).content)
                    messagebox.showinfo("Download Complete", "Update downloaded successfully.")
        else:
            messagebox.showerror("Error", "Failed to check for updates. Please try again later.")

if __name__ == "__main__":
    app = MEOWCompressorApp()
    app.mainloop()
