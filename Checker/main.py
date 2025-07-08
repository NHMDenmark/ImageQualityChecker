import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys
import random
import threading
from BlackLineFinder import black_line_finder
from FileChecker import file_checker

script_dir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)

# GUI class
class BlackLineFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Quality Checker")

        self.folder_path = tk.StringVar()
        self.top_margin = tk.StringVar()
        self.bottom_margin = tk.StringVar()

        self.last_run_state = {"folder": None, "top": None, "bottom": None}

        self.happy_msg = self.create_happiness()
        
        # Choose folder button
        self.choose_button = tk.Button(root, text="Choose Folder", command=self.choose_folder)
        self.choose_button.pack(pady=10)

        # Label to show selected folder
        self.folder_label = tk.Label(root, text="No folder selected")
        self.folder_label.pack()

        # Margin inputs
        self.top_entry = self._make_labeled_entry("Top Margin to exclude(%)", self.top_margin)
        self.bottom_entry = self._make_labeled_entry("Bottom Margin to exclude(%)", self.bottom_margin)

        # Progress bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)
        self.progress["value"] = 0
        self.progress["maximum"] = 100  # Will be set dynamically later

        # Run button
        self.run_button = tk.Button(root, text="Run Image Checker", command=self.run_script, state=tk.DISABLED)
        self.run_button.pack(pady=10)

        # Track input changes
        self.folder_path.trace_add("write", lambda *args: self._check_if_ready())
        self.top_margin.trace_add("write", lambda *args: self._check_if_ready())
        self.bottom_margin.trace_add("write", lambda *args: self._check_if_ready())

    def _make_labeled_entry(self, label_text, variable):
        frame = tk.Frame(self.root)
        frame.pack()
        tk.Label(frame, text=label_text).pack(side=tk.LEFT)
        entry = tk.Entry(frame, textvariable=variable, width=5)
        entry.pack(side=tk.LEFT)
        return entry

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
            self.folder_label.config(text=folder)

    def _check_if_ready(self):
        folder = self.folder_path.get()
        top = self.top_margin.get()
        bottom = self.bottom_margin.get()

        if not folder:
            self.run_button.config(state=tk.DISABLED)
            return

        if (
            folder != self.last_run_state["folder"] or
            top != self.last_run_state["top"] or
            bottom != self.last_run_state["bottom"]
        ):
            self.run_button.config(state=tk.NORMAL)
        else:
            self.run_button.config(state=tk.DISABLED)

    def run_script(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showwarning("Warning", "Please choose a folder first.")
            return

        # Validate input
        try:
            top_margin = int(self.top_margin.get())
            bottom_margin = int(self.bottom_margin.get())
        except ValueError:
            messagebox.showerror("Error", "Top and bottom margins must be integers.")
            return

         # Save current state to prevent duplicate runs
        self.last_run_state = {
            "folder": folder,
            "top": self.top_margin.get(),
            "bottom": self.bottom_margin.get()
        }

        self.run_button.config(state=tk.DISABLED)
        threading.Thread(target=self._run_script_thread, args=(folder, top_margin, bottom_margin), daemon=True).start()

    def _run_script_thread(self, folder, top, bottom):
        try:
            files = []
            for ext in [".tif", ".tiff", ".cr2", ".cr3", ".raf", ".jpg", ".jpeg"]:
                files.extend([f for f in os.listdir(folder) if f.lower().endswith(ext)])
            
            total = len(files)

            if total == 0:
                self._show_popup("No image files found in the folder.")
                return

            self.progress["maximum"] = total
            self.progress["value"] = 0

            f_checker = file_checker.FileChecker(folder)
            fc = f_checker.check_matching_files()

            blf = black_line_finder.BlackLineFinder(
                folder,
                top_margin_percent=top,
                bottom_margin_percent=bottom
            )

            OUTPUT_FILE = os.path.join(folder, f"{os.path.basename(os.path.normpath(folder))}.txt")
            black_lines = False
            first_black_line = True

            for idx, filename in enumerate(files, start=1):
                image_path = os.path.join(folder, filename)
                if blf.detect_black_lines(image_path):
                    with open(OUTPUT_FILE, 'a') as f:
                        if first_black_line:
                            f.write(f"\nBlack lines:\n")
                            first_black_line = False
                        f.write(f"{filename}\n")
                        black_lines = True

                # Update progress bar on UI thread
                self.root.after(0, self.progress.step, 1)

            self._show_popup(f"{os.path.basename(os.path.normpath(folder))} completed! \nFound black lines: {black_lines} \nMissing files(json/tif): {fc} \n\n{self.happy_msg}")
        except Exception as e:
            self._show_popup(f"Something went wrong for {os.path.basename(os.path.normpath(folder))}:\n{str(e)}", error=True)

        self.root.after(0, self._check_if_ready)

    def create_happiness(self):

        noun = ["A penguin", "A lion", "A sealion", "A biologist", "A puppy", "A goldfish", "A cat", "The sun", "A ghost", "A dragon", "A bumble-bee", "A narwhal"]

        verb = ["is waving", "is smiling", "is winking", "is basking", "is dancing", "is jumping", "is singing"]

        adjective = ["happily", "sweetly", "joyfully", "excitedly", "playfully", "cheerfully", "gently", "gracefully", "enthusiastically"]

        n = noun[random.randint(0,len(noun)-1)]
        v = verb[random.randint(0,len(verb)-1)]
        a = adjective[random.randint(0,len(adjective)-1)]
        
        poetry = f"{n} {v} {a}."

        return poetry

    def _show_popup(self, message, error=False):
        def show():
            self.progress["value"] = 0  # Reset progress
            if error:
                messagebox.showerror("Error", message)
            else:
                messagebox.showinfo("Success", message)
        self.root.after(0, show)

# Main app
if __name__ == "__main__":
    root = tk.Tk()
    app = BlackLineFinderApp(root)
    root.mainloop()
