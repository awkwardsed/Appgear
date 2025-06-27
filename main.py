import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

class AppImageLauncherMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("AppImage Launcher Maker")

        # Select AppImage
        self.appimage_path = ""
        self.select_button = tk.Button(root, text="Select AppImage", command=self.select_appimage)
        self.select_button.pack()

        # Name Entry
        self.name_label = tk.Label(root, text="Launcher Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(root)
        self.name_entry.pack()

        # Icon Entry
        self.icon_label = tk.Label(root, text="Icon Path:")
        self.icon_label.pack()
        self.icon_entry = tk.Entry(root)
        self.icon_entry.pack()
        self.icon_button = tk.Button(root, text="Select Icon", command=self.select_icon)
        self.icon_button.pack()

        # Create Launcher Button
        self.create_button = tk.Button(root, text="Create Launcher", command=self.create_launcher)
        self.create_button.pack()

    def select_appimage(self):
        self.appimage_path = filedialog.askopenfilename(title="Select AppImage", filetypes=[("AppImage files", "*.AppImage")])
        if self.appimage_path:
            messagebox.showinfo("Selected AppImage", self.appimage_path)

    def select_icon(self):
        icon_path = filedialog.askopenfilename(title="Select Icon", filetypes=[("Image files", "*.png;*.svg")])
        if icon_path:
            self.icon_entry.delete(0, tk.END)
            self.icon_entry.insert(0, icon_path)

    def create_launcher(self):
        name = self.name_entry.get()
        icon = self.icon_entry.get()

        if not self.appimage_path or not name or not icon:
            messagebox.showerror("Error", "Please fill all fields and select an AppImage.")
            return

        # Make AppImage executable
        os.chmod(self.appimage_path, 0o755)

        # Create .desktop file
        desktop_entry = f"""
[Desktop Entry]
Name={name}
Exec={self.appimage_path}
Icon={icon}
Type=Application
Categories=Utility;
"""
        desktop_file_path = os.path.join(os.path.expanduser("~/.local/share/applications"), f"{name}.desktop")
        with open(desktop_file_path, "w") as f:
            f.write(desktop_entry.strip())

        # Update desktop database
        subprocess.run(["update-desktop-database", os.path.dirname(desktop_file_path)])

        messagebox.showinfo("Success", f"Launcher created: {desktop_file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppImageLauncherMaker(root)
    root.mainloop()

