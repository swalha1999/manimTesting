import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import threading
import subprocess
from idlelib.colorizer import ColorDelegator
from idlelib.percolator import Percolator
from tkVideoPlayer import TkinterVideo
import os

class ManimGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Manim GUI")
        self.root.geometry("800x600")  # Set the window size

        # Create a scrolled text widget for code input
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
        self.text_area.grid(column=0, row=0, padx=10, pady=10, columnspan=2)

        # Add syntax highlighting
        Percolator(self.text_area).insertfilter(ColorDelegator())

        # Create a button to select a file
        self.file_button = tk.Button(root, text="Select File", command=self.select_file)
        self.file_button.grid(column=0, row=1, padx=10, pady=10, sticky="ew")

        # Create a button to run the scene
        self.run_button = tk.Button(root, text="Run Scene", command=self.run_scene)
        self.run_button.grid(column=1, row=1, padx=10, pady=10, sticky="ew")

        # Create a video player widget
        self.video_player = TkinterVideo(master=root, scaled=True)
        self.video_player.grid(column=0, row=2, padx=10, pady=10, columnspan=2)
        
        # Store the selected file path
        self.selected_file = None

    def select_file(self):
        # Prompt the user to select a Python file
        self.selected_file = filedialog.askopenfilename(
            title="Select a Manim Scene File",
            filetypes=(("Python Files", "*.py"), ("All Files", "*.*"))
        )
        if self.selected_file:
            # Load the content of the file into the text area
            with open(self.selected_file, 'r') as file:
                code = file.read()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, code)

    def run_scene(self):
        if not self.selected_file:
            messagebox.showerror("Error", "No file selected!")
            return
        
        # Save the code from the text area back to the selected file
        code = self.text_area.get("1.0", tk.END)
        with open(self.selected_file, "w") as f:
            f.write(code)
        
        # Extract the scene name from the selected file (you might need a custom way to determine the scene class)
        scene_name = self.extract_scene_name(code)
        
        # Run the Manim scene in a separate thread to avoid blocking the GUI
        threading.Thread(target=self.execute_manim, args=(self.selected_file, scene_name)).start()

    def extract_scene_name(self, code):
        # A simple way to extract the class name; you might need a more robust method
        for line in code.split('\n'):
            if line.strip().startswith("class "):
                return line.split()[1].split('(')[0]
        return "SceneClassName"

    def execute_manim(self, filename, scene_name):
        try:
            subprocess.run(["manim", "-ql", filename, scene_name], check=True)
            messagebox.showinfo("Success", "Scene rendered successfully!")
            self.play_video(scene_name)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to render scene: {e}")

    def play_video(self, scene_name):
        video_path = f"media/videos/{os.path.basename(self.selected_file).replace('.py', '')}/480p30/{scene_name}.mp4"
        if os.path.exists(video_path):
            self.video_player.load(video_path)
            self.video_player.play()
        else:
            messagebox.showerror("Error", "Video file not found!")

# Create the main window
root = tk.Tk()
app = ManimGUI(root)
root.mainloop()
