"""
Image Recognition Application

A simple GUI application for recognizing objects in images using
pre-trained deep learning models.
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import threading

from image_recognition import ImageRecognizer


class ImageRecognitionApp:
    """Main application class for the image recognition GUI."""
    
    def __init__(self, root):
        """
        Initialize the application.
        
        Args:
            root: The tkinter root window.
        """
        self.root = root
        self.root.title("画像認識アプリ")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        
        self.recognizer = ImageRecognizer()
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="画像認識アプリ", 
            font=("Helvetica", 16)
        )
        title_label.pack(pady=10)
        
        # Instructions
        instructions = ttk.Label(
            main_frame,
            text="画像を選択して、認識を開始してください。",
            font=("Helvetica", 10)
        )
        instructions.pack(pady=5)
        
        # Image selection frame
        select_frame = ttk.Frame(main_frame)
        select_frame.pack(fill=tk.X, pady=10)
        
        self.path_var = tk.StringVar()
        path_entry = ttk.Entry(select_frame, textvariable=self.path_var, width=50)
        path_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_button = ttk.Button(
            select_frame, 
            text="参照...", 
            command=self.browse_image
        )
        browse_button.pack(side=tk.RIGHT, padx=5)
        
        # Image display area
        self.image_frame = ttk.LabelFrame(main_frame, text="画像プレビュー")
        self.image_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.image_label = ttk.Label(self.image_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Results area
        results_frame = ttk.LabelFrame(main_frame, text="認識結果")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.results_text = tk.Text(results_frame, height=10, wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.recognize_button = ttk.Button(
            button_frame, 
            text="認識開始", 
            command=self.start_recognition,
            state=tk.DISABLED
        )
        self.recognize_button.pack(side=tk.RIGHT, padx=5)
        
        clear_button = ttk.Button(
            button_frame, 
            text="クリア", 
            command=self.clear_all
        )
        clear_button.pack(side=tk.RIGHT, padx=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame, 
            orient=tk.HORIZONTAL, 
            length=100, 
            mode='indeterminate',
            variable=self.progress_var
        )
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("準備完了")
        status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def browse_image(self):
        """Open a file dialog to select an image."""
        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
            ("All files", "*.*")
        ]
        filename = filedialog.askopenfilename(
            title="画像ファイルを選択",
            filetypes=filetypes
        )
        
        if filename:
            self.path_var.set(filename)
            self.load_preview(filename)
            self.recognize_button.config(state=tk.NORMAL)
            self.status_var.set(f"画像を選択しました: {os.path.basename(filename)}")
    
    def load_preview(self, image_path):
        """
        Load and display a preview of the selected image.
        
        Args:
            image_path (str): Path to the image file.
        """
        try:
            # Open and resize the image for preview
            img = Image.open(image_path)
            img.thumbnail((400, 400))  # Resize for preview
            photo = ImageTk.PhotoImage(img)
            
            # Update the image label
            self.image_label.config(image=photo)
            self.image_label.image = photo  # Keep a reference
        except Exception as e:
            messagebox.showerror("エラー", f"画像を読み込めませんでした: {str(e)}")
    
    def start_recognition(self):
        """Start the image recognition process in a separate thread."""
        image_path = self.path_var.get()
        if not image_path or not os.path.exists(image_path):
            messagebox.showerror("エラー", "有効な画像ファイルを選択してください。")
            return
        
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        self.status_var.set("認識中...")
        self.recognize_button.config(state=tk.DISABLED)
        
        # Start progress bar
        self.progress_bar.start()
        
        # Run recognition in a separate thread
        thread = threading.Thread(target=self.run_recognition, args=(image_path,))
        thread.daemon = True
        thread.start()
    
    def run_recognition(self, image_path):
        """
        Run the image recognition process.
        
        Args:
            image_path (str): Path to the image file.
        """
        try:
            results = self.recognizer.recognize(image_path)
            
            # Update UI in the main thread
            self.root.after(0, lambda: self.display_results(results))
        except Exception as e:
            self.root.after(0, lambda: self.show_error(str(e)))
    
    def display_results(self, results):
        """
        Display recognition results in the UI.
        
        Args:
            results (list): List of recognition results.
        """
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "===== 認識結果 =====\n\n")
        
        for i, (_, description, score) in enumerate(results, 1):
            confidence = score * 100
            self.results_text.insert(
                tk.END, 
                f"{i}. {description} ({confidence:.2f}% 確信度)\n"
            )
        
        self.progress_bar.stop()
        self.recognize_button.config(state=tk.NORMAL)
        self.status_var.set("認識完了")
    
    def show_error(self, error_message):
        """
        Display an error message.
        
        Args:
            error_message (str): The error message to display.
        """
        self.progress_bar.stop()
        self.recognize_button.config(state=tk.NORMAL)
        self.status_var.set("エラーが発生しました")
        messagebox.showerror("エラー", f"認識中にエラーが発生しました: {error_message}")
    
    def clear_all(self):
        """Clear all fields and reset the application state."""
        self.path_var.set("")
        self.image_label.config(image="")
        self.results_text.delete(1.0, tk.END)
        self.recognize_button.config(state=tk.DISABLED)
        self.status_var.set("準備完了")


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = ImageRecognitionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()