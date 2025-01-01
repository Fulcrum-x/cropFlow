import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import os
import numpy as np
import cv2
from pathlib import Path

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("cropFlow")
        self.root.geometry("600x500")
        
        # Aspect ratio options
        self.aspect_ratios = {
            "Default (Keep Original)": None,
            "16:9": 16/9,
            "1.85:1": 1.85/1,
            "2.39:1": 2.39/1,
            "4:3": 4/3,
            "Auto-detect Letterbox": "auto"
        }
        
        # Tone mapping options
        self.tone_mapping_methods = {
            "None": None,
            "Drago": 1,    # cv2.TONEMAP_DRAGO
            "Reinhard": 2, # cv2.TONEMAP_REINHARD
            "Mantiuk": 3   # cv2.TONEMAP_MANTIUK
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Folder selection
        ttk.Label(main_frame, text="Select folder with PNG images:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.folder_path = tk.StringVar()
        folder_entry = ttk.Entry(main_frame, textvariable=self.folder_path, width=50)
        folder_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_folder).grid(row=1, column=1, padx=5)
        
        # Aspect ratio selection
        ttk.Label(main_frame, text="Select aspect ratio:").grid(row=2, column=0, sticky=tk.W, pady=(15,5))
        self.aspect_ratio_var = tk.StringVar(value="Default (Keep Original)")
        aspect_combo = ttk.Combobox(main_frame, textvariable=self.aspect_ratio_var, values=list(self.aspect_ratios.keys()))
        aspect_combo.grid(row=3, column=0, sticky=(tk.W, tk.E), padx=5)
        
        # Tone mapping selection
        ttk.Label(main_frame, text="HDR Tone Mapping:").grid(row=4, column=0, sticky=tk.W, pady=(15,5))
        self.tone_mapping_var = tk.StringVar(value="Reinhard")
        tone_mapping_combo = ttk.Combobox(main_frame, textvariable=self.tone_mapping_var, values=list(self.tone_mapping_methods.keys()))
        tone_mapping_combo.grid(row=5, column=0, sticky=(tk.W, tk.E), padx=5)
        tone_mapping_combo.bind('<<ComboboxSelected>>', self.on_tone_mapping_change)
        
        # Tone mapping parameters
        self.intensity_label = ttk.Label(main_frame, text="Tone Mapping Intensity:")
        self.intensity_label.grid(row=6, column=0, sticky=tk.W, pady=(15,5))
        self.gamma_var = tk.DoubleVar(value=0.5)  # Lower default value
        self.gamma_spin = ttk.Spinbox(main_frame, from_=0.1, to=3.0, increment=0.1, textvariable=self.gamma_var, width=10)
        self.gamma_spin.grid(row=7, column=0, sticky=tk.W, padx=5)
        
        # Quality selection
        ttk.Label(main_frame, text="JPEG Quality (1-100):").grid(row=8, column=0, sticky=tk.W, pady=(15,5))
        self.quality_var = tk.IntVar(value=95)
        quality_spin = ttk.Spinbox(main_frame, from_=1, to=100, textvariable=self.quality_var, width=10)
        quality_spin.grid(row=9, column=0, sticky=tk.W, padx=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress.grid(row=10, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=20)
        
        # Convert button
        self.convert_btn = ttk.Button(main_frame, text="Convert Images", command=self.convert_images)
        self.convert_btn.grid(row=11, column=0, columnspan=2, pady=10)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def detect_letterbox(self, img):
        # Convert image to numpy array
        img_array = np.array(img)
        
        # Check for horizontal letterbox (black bars on top/bottom)
        rows = np.mean(img_array, axis=(1, 2))
        black_rows = np.where(rows < 10)[0]
        
        if len(black_rows) > 0:
            top = 0
            bottom = img_array.shape[0]
            
            # Find top letterbox
            for i in black_rows:
                if i == top:
                    top += 1
                else:
                    break
                    
            # Find bottom letterbox
            for i in reversed(black_rows):
                if i == bottom - 1:
                    bottom -= 1
                else:
                    break
                    
            return img.crop((0, top, img.width, bottom))
        
        return img

    def on_tone_mapping_change(self, event=None):
        # Enable/disable intensity control based on tone mapping selection
        if self.tone_mapping_var.get() == "None":
            self.gamma_spin.configure(state="disabled")
            self.intensity_label.configure(state="disabled")
        else:
            self.gamma_spin.configure(state="normal")
            self.intensity_label.configure(state="normal")

    def apply_tone_mapping(self, img_array):
        # Convert to float32 and normalize
        img_float32 = img_array.astype(np.float32) / 255.0
        
        # Create tone mapping operator
        tone_map_method = self.tone_mapping_methods[self.tone_mapping_var.get()]
        if tone_map_method is None:
            return img_array
            
        try:
            if tone_map_method == 1:  # Drago
                tonemapper = cv2.createTonemapDrago(gamma=self.gamma_var.get(), saturation=1.0)
            elif tone_map_method == 2:  # Reinhard
                # Adjusted parameters for Reinhard
                intensity = self.gamma_var.get()
                tonemapper = cv2.createTonemapReinhard(
                    gamma=intensity,
                    intensity=intensity * 0.5,  # Reduced intensity to prevent blow-out
                    light_adapt=0.8,
                    color_adapt=0.5
                )
            elif tone_map_method == 3:  # Mantiuk
                tonemapper = cv2.createTonemapMantiuk(gamma=self.gamma_var.get(), saturation=1.0, scale=0.7)
        except AttributeError:
            # Fallback to Reinhard if specific method not available
            intensity = self.gamma_var.get()
            tonemapper = cv2.createTonemapReinhard(
                gamma=intensity,
                intensity=intensity * 0.5,
                light_adapt=0.8,
                color_adapt=0.5
            )
        
        # Apply tone mapping
        tone_mapped = tonemapper.process(img_float32)
        
        # Improve color preservation
        tone_mapped = np.clip(tone_mapped * 255, 0, 255).astype(np.uint8)
        
        return tone_mapped

    def crop_to_aspect_ratio(self, img, target_ratio):
        if target_ratio is None:
            return img
            
        if target_ratio == "auto":
            return self.detect_letterbox(img)
            
        current_ratio = img.width / img.height
        
        if abs(current_ratio - target_ratio) < 0.01:
            return img
            
        if current_ratio > target_ratio:
            # Image is too wide, crop width
            new_width = int(img.height * target_ratio)
            left = (img.width - new_width) // 2
            return img.crop((left, 0, left + new_width, img.height))
        else:
            # Image is too tall, crop height
            new_height = int(img.width / target_ratio)
            top = (img.height - new_height) // 2
            return img.crop((0, top, img.width, top + new_height))

    def convert_images(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showerror("Error", "Please select a folder first!")
            return
            
        png_files = list(Path(folder).glob("*.png"))
        if not png_files:
            messagebox.showinfo("Info", "No PNG files found in the selected folder!")
            return
            
        aspect_ratio = self.aspect_ratios[self.aspect_ratio_var.get()]
        quality = self.quality_var.get()
        
        self.convert_btn.config(state='disabled')
        processed = 0
        
        for png_file in png_files:
            try:
                # Open and convert image
                with Image.open(png_file) as img:
                    # Convert to RGB if necessary
                    if img.mode in ('RGBA', 'LA'):
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1])
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Convert to numpy array for tone mapping
                    img_array = np.array(img)
                    
                    # Apply tone mapping
                    tone_mapped = self.apply_tone_mapping(img_array)
                    
                    # Convert back to PIL Image
                    img = Image.fromarray(tone_mapped)
                    
                    # Crop to aspect ratio if selected
                    img = self.crop_to_aspect_ratio(img, aspect_ratio)
                    
                    # Save as JPG
                    jpg_path = png_file.with_suffix('.jpg')
                    img.save(jpg_path, 'JPEG', quality=quality)
                
                processed += 1
                self.progress_var.set((processed / len(png_files)) * 100)
                self.root.update()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error processing {png_file.name}: {str(e)}")
                
        self.convert_btn.config(state='normal')
        messagebox.showinfo("Success", f"Converted {processed} images successfully!")
        self.progress_var.set(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()