import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import threading
import time
from datetime import datetime
import json

class AdvancedFileSorter:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced File Sorter - by Syed Dayim")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # File type mappings
        self.file_types = {
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp', '.ico'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
            'Music': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
            'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb', '.go'],
            'Executables': ['.exe', '.msi', '.dmg', '.deb', '.rpm', '.app']
        }
        
        # Settings
        self.settings_file = 'file_sorter_settings.json'
        self.load_settings()
        
        # Operation history for undo
        self.operation_history = []
        
        self.setup_ui()
        
    def load_settings(self):
        """Load settings from JSON file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.file_types = settings.get('file_types', self.file_types)
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save_settings(self):
        """Save settings to JSON file"""
        try:
            settings = {'file_types': self.file_types}
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Advanced File Sorter - by Syed Dayim", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Developer info
        dev_info_label = ttk.Label(main_frame, text="Email: dayim1277@gmail.com | GitHub: github.com/syedDayim", 
                                 font=('Arial', 9))
        dev_info_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        
        # Directory selection
        ttk.Label(main_frame, text="Select Directory:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.directory_var = tk.StringVar()
        self.directory_entry = ttk.Entry(main_frame, textvariable=self.directory_var, width=50)
        self.directory_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        
        browse_btn = ttk.Button(main_frame, text="Browse", command=self.browse_directory)
        browse_btn.grid(row=2, column=2, padx=(5, 0), pady=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        options_frame.columnconfigure(1, weight=1)
        
        # Preview mode checkbox
        self.preview_mode = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Preview Mode (recommended)", 
                       variable=self.preview_mode).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        # Create folders checkbox
        self.create_folders = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Create folders automatically", 
                       variable=self.create_folders).grid(row=1, column=0, sticky=tk.W, pady=2)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        self.preview_btn = ttk.Button(button_frame, text="Preview Files", 
                                     command=self.preview_files, style='Accent.TButton')
        self.preview_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.sort_btn = ttk.Button(button_frame, text="Sort Files", 
                                  command=self.sort_files, style='Accent.TButton')
        self.sort_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.undo_btn = ttk.Button(button_frame, text="Undo Last Operation", 
                                  command=self.undo_last_operation)
        self.undo_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        settings_btn = ttk.Button(button_frame, text="Settings", 
                                 command=self.open_settings)
        settings_btn.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=6, column=0, columnspan=3, pady=5)
        
        # Results text area
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="5")
        results_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(7, weight=1)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, width=80)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure styles
        style = ttk.Style()
        style.configure('Accent.TButton', foreground='white', background='#0078d4')
    
    def browse_directory(self):
        """Open directory browser"""
        directory = filedialog.askdirectory()
        if directory:
            self.directory_var.set(directory)
    
    def get_file_category(self, file_path):
        """Determine file category based on extension"""
        file_ext = Path(file_path).suffix.lower()
        for category, extensions in self.file_types.items():
            if file_ext in extensions:
                return category
        return 'Other'
    
    def scan_directory(self, directory):
        """Scan directory for files to sort"""
        files_to_sort = {}
        total_files = 0
        
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    category = self.get_file_category(file_path)
                    
                    if category not in files_to_sort:
                        files_to_sort[category] = []
                    
                    files_to_sort[category].append(file_path)
                    total_files += 1
                    
        except Exception as e:
            self.log_message(f"Error scanning directory: {e}")
            return {}, 0
            
        return files_to_sort, total_files
    
    def preview_files(self):
        """Preview files that will be sorted"""
        directory = self.directory_var.get()
        if not directory or not os.path.exists(directory):
            messagebox.showerror("Error", "Please select a valid directory")
            return
        
        self.log_message("Scanning directory for files...")
        self.status_var.set("Scanning...")
        self.progress_var.set(0)
        
        # Run in separate thread to prevent UI freezing
        threading.Thread(target=self._preview_files_thread, daemon=True).start()
    
    def _preview_files_thread(self):
        """Preview files in separate thread"""
        try:
            directory = self.directory_var.get()
            files_to_sort, total_files = self.scan_directory(directory)
            
            self.root.after(0, self._update_preview_results, files_to_sort, total_files)
            
        except Exception as e:
            self.root.after(0, self.log_message, f"Error during preview: {e}")
            self.root.after(0, lambda: self.status_var.set("Error"))
    
    def _update_preview_results(self, files_to_sort, total_files):
        """Update preview results in main thread"""
        self.results_text.delete(1.0, tk.END)
        
        if total_files == 0:
            self.log_message("No files found to sort.")
            self.status_var.set("No files found")
            return
        
        self.log_message(f"Found {total_files} files to sort:")
        self.log_message("=" * 50)
        
        directory = self.directory_var.get()
        files_to_move = 0
        files_already_sorted = 0
        
        for category, files in files_to_sort.items():
            if files:
                self.log_message(f"\n{category} ({len(files)} files):")
                category_folder = os.path.join(directory, category)
                
                for file_path in files[:10]:  # Show first 10 files
                    filename = os.path.basename(file_path)
                    file_dir = os.path.dirname(file_path)
                    
                    # Check if file is already in correct folder
                    if file_dir == category_folder:
                        self.log_message(f"  ✓ {filename} (already sorted)")
                        files_already_sorted += 1
                    else:
                        self.log_message(f"  → {filename} (will move to {category}/)")
                        files_to_move += 1
                
                if len(files) > 10:
                    # Count remaining files
                    remaining_files = files[10:]
                    for file_path in remaining_files:
                        file_dir = os.path.dirname(file_path)
                        if file_dir == category_folder:
                            files_already_sorted += 1
                        else:
                            files_to_move += 1
                    
                    self.log_message(f"  ... and {len(files) - 10} more files")
        
        self.log_message(f"\nSummary:")
        self.log_message(f"  Files to move: {files_to_move}")
        self.log_message(f"  Files already sorted: {files_already_sorted}")
        
        self.status_var.set(f"Preview complete - {total_files} files found ({files_to_move} to move)")
        self.progress_var.set(100)
    
    def sort_files(self):
        """Sort files into categories"""
        directory = self.directory_var.get()
        if not directory or not os.path.exists(directory):
            messagebox.showerror("Error", "Please select a valid directory")
            return
        
        if not self.preview_mode.get():
            result = messagebox.askyesno("Confirm", 
                                       "Are you sure you want to sort files without preview?")
            if not result:
                return
        
        self.log_message("Starting file sorting...")
        self.status_var.set("Sorting files...")
        self.progress_var.set(0)
        
        # Run in separate thread
        threading.Thread(target=self._sort_files_thread, daemon=True).start()
    
    def _sort_files_thread(self):
        """Sort files in separate thread"""
        try:
            directory = self.directory_var.get()
            files_to_sort, total_files = self.scan_directory(directory)
            
            if total_files == 0:
                self.root.after(0, self.log_message, "No files found to sort.")
                self.root.after(0, lambda: self.status_var.set("No files found"))
                return
            
            # Create operation record for undo
            operation_record = {
                'timestamp': datetime.now().isoformat(),
                'moves': []
            }
            
            moved_files = 0
            skipped_files = 0
            
            for category, files in files_to_sort.items():
                if not files:
                    continue
                
                # Create category folder if needed
                category_folder = os.path.join(directory, category)
                if self.create_folders.get() and not os.path.exists(category_folder):
                    os.makedirs(category_folder)
                    self.root.after(0, self.log_message, f"Created folder: {category}")
                
                # Move files
                for file_path in files:
                    try:
                        # Check if file is already in the correct category folder
                        file_dir = os.path.dirname(file_path)
                        if file_dir == category_folder:
                            skipped_files += 1
                            continue
                        
                        filename = os.path.basename(file_path)
                        destination = os.path.join(category_folder, filename)
                        
                        # Handle duplicate filenames
                        counter = 1
                        original_destination = destination
                        while os.path.exists(destination):
                            name, ext = os.path.splitext(filename)
                            destination = os.path.join(category_folder, f"{name}_{counter}{ext}")
                            counter += 1
                        
                        # Record the move for undo
                        operation_record['moves'].append({
                            'from': file_path,
                            'to': destination
                        })
                        
                        shutil.move(file_path, destination)
                        moved_files += 1
                        
                        # Update progress
                        progress = (moved_files / total_files) * 100
                        self.root.after(0, lambda p=progress: self.progress_var.set(p))
                        
                        if moved_files % 10 == 0:  # Update status every 10 files
                            self.root.after(0, self.log_message, 
                                          f"Moved {moved_files}/{total_files} files...")
                        
                    except Exception as e:
                        self.root.after(0, self.log_message, 
                                      f"Error moving {os.path.basename(file_path)}: {e}")
            
            # Save operation for undo
            if operation_record['moves']:
                self.operation_history.append(operation_record)
                # Keep only last 10 operations
                if len(self.operation_history) > 10:
                    self.operation_history.pop(0)
            
            self.root.after(0, self._sort_complete, moved_files, total_files, skipped_files)
            
        except Exception as e:
            self.root.after(0, self.log_message, f"Error during sorting: {e}")
            self.root.after(0, lambda: self.status_var.set("Error"))
    
    def _sort_complete(self, moved_files, total_files, skipped_files=0):
        """Handle sort completion"""
        self.log_message(f"\nSorting complete! Moved {moved_files} files.")
        if skipped_files > 0:
            self.log_message(f"Skipped {skipped_files} files that were already in correct folders.")
        self.status_var.set(f"Complete - {moved_files} files moved")
        self.progress_var.set(100)
        
        if moved_files < total_files:
            remaining = total_files - moved_files - skipped_files
            if remaining > 0:
                self.log_message(f"Note: {remaining} files could not be moved.")
    
    def undo_last_operation(self):
        """Undo the last sorting operation"""
        if not self.operation_history:
            messagebox.showinfo("Info", "No operations to undo")
            return
        
        result = messagebox.askyesno("Confirm Undo", 
                                   "Are you sure you want to undo the last operation?")
        if not result:
            return
        
        operation = self.operation_history.pop()
        self.log_message("Undoing last operation...")
        self.status_var.set("Undoing...")
        
        # Run undo in separate thread
        threading.Thread(target=self._undo_operation, args=(operation,), daemon=True).start()
    
    def _undo_operation(self, operation):
        """Undo operation in separate thread"""
        try:
            moved_back = 0
            for move in reversed(operation['moves']):  # Reverse order
                try:
                    shutil.move(move['to'], move['from'])
                    moved_back += 1
                except Exception as e:
                    self.root.after(0, self.log_message, 
                                  f"Error undoing move: {e}")
            
            self.root.after(0, self.log_message, 
                          f"Undo complete! Moved {moved_back} files back.")
            self.root.after(0, lambda: self.status_var.set("Undo complete"))
            
        except Exception as e:
            self.root.after(0, self.log_message, f"Error during undo: {e}")
            self.root.after(0, lambda: self.status_var.set("Undo error"))
    
    def open_settings(self):
        """Open settings window"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("File Sorter Settings")
        settings_window.geometry("600x500")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Create notebook for tabs
        notebook = ttk.Notebook(settings_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # File types tab
        file_types_frame = ttk.Frame(notebook)
        notebook.add(file_types_frame, text="File Types")
        
        # Create scrollable frame for file types
        canvas = tk.Canvas(file_types_frame)
        scrollbar = ttk.Scrollbar(file_types_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # File type entries
        self.file_type_vars = {}
        row = 0
        
        for category, extensions in self.file_types.items():
            ttk.Label(scrollable_frame, text=f"{category}:", 
                     font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=5)
            
            var = tk.StringVar(value=', '.join(extensions))
            entry = ttk.Entry(scrollable_frame, textvariable=var, width=50)
            entry.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
            self.file_type_vars[category] = var
            row += 1
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Buttons
        button_frame = ttk.Frame(settings_window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Save", 
                  command=lambda: self.save_settings_from_window(settings_window)).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", 
                  command=settings_window.destroy).pack(side=tk.RIGHT)
    
    def save_settings_from_window(self, window):
        """Save settings from settings window"""
        try:
            for category, var in self.file_type_vars.items():
                extensions = [ext.strip() for ext in var.get().split(',') if ext.strip()]
                self.file_types[category] = extensions
            
            self.save_settings()
            messagebox.showinfo("Success", "Settings saved successfully!")
            window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error saving settings: {e}")
    
    def log_message(self, message):
        """Add message to results text area"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.results_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.results_text.see(tk.END)

def main():
    root = tk.Tk()
    app = AdvancedFileSorter(root)
    root.mainloop()

if __name__ == "__main__":
    main()