import os
import json
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import webbrowser
from PyPDF2 import PdfMerger
import pandas as pd

SESSION_FILE = "session.json"

class ModernFileManager:
    def __init__(self, root):
        self.root = root
        self.root.title("File Merger Studio")
        self.root.geometry("1024x768")
        self.root.minsize(800, 600)
        self.root.configure(bg='#1a1a1a')
        #need scrollbar
        self.root.resizable(True, True)
        
        # App state
        self.pdf_files = []
        self.excel_files = []
        self.current_tab = "pdf"
        
        # Configure styles
        self.setup_styles()
        self.create_ui()
        self.load_session()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Dark theme colors
        colors = {
            'bg': '#1a1a1a',
            'surface': '#2d2d2d',
            'primary': '#3b82f6',
            'primary_hover': '#2563eb',
            'success': '#10b981',
            'danger': '#ef4444',
            'text': '#ffffff',
            'text_secondary': '#a1a1aa',
            'border': '#404040'
        }
        
        # Configure styles
        self.style.configure('Dark.TFrame', background=colors['bg'])
        self.style.configure('Surface.TFrame', background=colors['surface'], relief='flat')
        
        self.style.configure('Title.TLabel', 
                           font=('Segoe UI', 24, 'bold'),
                           background=colors['bg'],
                           foreground=colors['text'])
        
        self.style.configure('Subtitle.TLabel',
                           font=('Segoe UI', 12),
                           background=colors['bg'],
                           foreground=colors['text_secondary'])
        
        self.style.configure('Tab.TButton',
                           font=('Segoe UI', 11, 'bold'),
                           background=colors['surface'],
                           foreground=colors['text'],
                           borderwidth=0,
                           focuscolor='none',
                           padding=(30, 15))
        
        self.style.configure('TabActive.TButton',
                           font=('Segoe UI', 11, 'bold'),
                           background=colors['primary'],
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none',
                           padding=(30, 15))
        
        self.style.configure('Action.TButton',
                           font=('Segoe UI', 11, 'bold'),
                           background=colors['primary'],
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none',
                           padding=(20, 12))
        
        self.style.configure('Success.TButton',
                           font=('Segoe UI', 11, 'bold'),
                           background=colors['success'],
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none',
                           padding=(20, 12))
        
        self.style.configure('Danger.TButton',
                           font=('Segoe UI', 10),
                           background=colors['danger'],
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none',
                           padding=(15, 8))

    def create_ui(self):
        # Main container
        main_container = ttk.Frame(self.root, style='Dark.TFrame')
        main_container.pack(fill='both', expand=True)
        
        # Header section
        self.create_header(main_container)
        
        # Tab navigation
        self.create_tab_navigation(main_container)
        
        # Content area
        self.create_content_area(main_container)
        
        # Footer
        self.create_footer(main_container)

    def create_header(self, parent):
        header_frame = ttk.Frame(parent, style='Dark.TFrame')
        header_frame.pack(fill='x', padx=40, pady=(30, 20))
        
        # App title and description
        title_label = ttk.Label(header_frame, text="File Merger Studio", style='Title.TLabel')
        title_label.pack(anchor='w')
        
        subtitle_label = ttk.Label(header_frame, 
                                  text="Merge multiple PDF or Excel files into one with ease",
                                  style='Subtitle.TLabel')
        subtitle_label.pack(anchor='w', pady=(5, 0))

    def create_tab_navigation(self, parent):
        tab_frame = ttk.Frame(parent, style='Dark.TFrame')
        tab_frame.pack(fill='x', padx=40, pady=(0, 30))
        
        # Tab buttons
        tab_container = ttk.Frame(tab_frame, style='Surface.TFrame')
        tab_container.pack(anchor='w')
        
        self.pdf_tab_btn = ttk.Button(tab_container, text="📄 PDF Merger",
                                     command=lambda: self.switch_tab("pdf"))
        self.pdf_tab_btn.pack(side='left')
        
        self.excel_tab_btn = ttk.Button(tab_container, text="📊 Excel Merger",
                                       command=lambda: self.switch_tab("excel"))
        self.excel_tab_btn.pack(side='left', padx=(2, 0))
        
        self.update_tab_styles()

    def create_content_area(self, parent):
        # Content container
        self.content_frame = ttk.Frame(parent, style='Dark.TFrame')
        self.content_frame.pack(fill='both', expand=True, padx=40)
        
        # File upload section
        self.create_upload_section()
        
        # File list section
        self.create_file_list_section()
        
        # Action buttons section
        self.create_action_section()

    def create_upload_section(self):
        upload_frame = ttk.Frame(self.content_frame, style='Surface.TFrame')
        upload_frame.pack(fill='x', pady=(0, 30), ipady=40)
        
        # Upload area
        upload_content = ttk.Frame(upload_frame, style='Surface.TFrame')
        upload_content.pack(expand=True)
        
        # Upload icon (using Unicode)
        icon_label = tk.Label(upload_content, text="📁", font=('Arial', 48),
                             bg='#2d2d2d', fg='#a1a1aa')
        icon_label.pack(pady=(20, 15))
        
        # Upload text
        upload_text = tk.Label(upload_content, 
                              text="Select files to merge",
                              font=('Segoe UI', 14, 'bold'),
                              bg='#2d2d2d', fg='#ffffff')
        upload_text.pack()
        
        desc_text = tk.Label(upload_content, 
                            text="Choose multiple files of the same type",
                            font=('Segoe UI', 11),
                            bg='#2d2d2d', fg='#a1a1aa')
        desc_text.pack(pady=(5, 20))
        
        # Select button
        self.select_btn = ttk.Button(upload_content, text="Select Files",
                                    style='Action.TButton',
                                    command=self.select_files)
        self.select_btn.pack(pady=(0, 20))

    def create_file_list_section(self):
        # File list header
        list_header = ttk.Frame(self.content_frame, style='Dark.TFrame')
        list_header.pack(fill='x', pady=(0, 15))
        
        self.files_title = tk.Label(list_header, text="Selected Files (0)",
                                   font=('Segoe UI', 14, 'bold'),
                                   bg='#1a1a1a', fg='#ffffff')
        self.files_title.pack(side='left')
        
        self.clear_btn = ttk.Button(list_header, text="Clear All",
                                   style='Danger.TButton',
                                   command=self.clear_all_files)
        self.clear_btn.pack(side='right')
        
        # Scrollable file list
        list_container = ttk.Frame(self.content_frame, style='Dark.TFrame')
        list_container.pack(fill='both', expand=True, pady=(0, 30))
        
        # Canvas for scrolling
        self.canvas = tk.Canvas(list_container, bg='#1a1a1a', highlightthickness=0, height=200)
        scrollbar = ttk.Scrollbar(list_container, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style='Dark.TFrame')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_action_section(self):
        action_frame = ttk.Frame(self.content_frame, style='Dark.TFrame')
        action_frame.pack(fill='x', pady=(0, 20))
        
        # Progress bar (initially hidden)
        self.progress_frame = ttk.Frame(action_frame, style='Dark.TFrame')
        
        self.progress_label = tk.Label(self.progress_frame, text="Processing...",
                                      font=('Segoe UI', 10),
                                      bg='#1a1a1a', fg='#a1a1aa')
        self.progress_label.pack(anchor='w', pady=(0, 5))
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, length=400)
        self.progress_bar.pack(fill='x')
        
        # Action buttons
        button_frame = ttk.Frame(action_frame, style='Dark.TFrame')
        button_frame.pack(fill='x', pady=(20, 0))
        
        self.merge_btn = ttk.Button(button_frame, text="🔗 Merge Files",
                                   style='Success.TButton',
                                   command=self.merge_files)
        self.merge_btn.pack(side='right')
        
        # File count and size info
        self.info_label = tk.Label(button_frame, text="No files selected",
                                  font=('Segoe UI', 10),
                                  bg='#1a1a1a', fg='#a1a1aa')
        self.info_label.pack(side='left', anchor='w')

    def create_footer(self, parent):
        footer_frame = ttk.Frame(parent, style='Dark.TFrame')
        footer_frame.pack(fill='x', padx=40, pady=(0, 20))
        
        # Separator line
        separator = tk.Frame(footer_frame, height=1, bg='#404040')
        separator.pack(fill='x', pady=(0, 15))
        
        # Footer content
        footer_content = ttk.Frame(footer_frame, style='Dark.TFrame')
        footer_content.pack(fill='x')
        
        credit_label = tk.Label(footer_content, 
                               text="Created by ScriptMalayali",
                               font=('Segoe UI', 10),
                               bg='#1a1a1a', fg='#3b82f6',
                               cursor='hand2')
        credit_label.pack(side='left')
        credit_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/scriptmalayali"))
        
        version_label = tk.Label(footer_content, 
                                text="v2.0",
                                font=('Segoe UI', 10),
                                bg='#1a1a1a', fg='#a1a1aa')
        version_label.pack(side='right')

    def switch_tab(self, tab):
        self.current_tab = tab
        self.update_tab_styles()
        self.update_select_button()
        self.update_file_display()

    def update_tab_styles(self):
        if self.current_tab == "pdf":
            self.pdf_tab_btn.configure(style='TabActive.TButton')
            self.excel_tab_btn.configure(style='Tab.TButton')
        else:
            self.excel_tab_btn.configure(style='TabActive.TButton')
            self.pdf_tab_btn.configure(style='Tab.TButton')

    def update_select_button(self):
        if self.current_tab == "pdf":
            self.select_btn.configure(text="Select PDF Files")
        else:
            self.select_btn.configure(text="Select Excel Files")

    def select_files(self):
        if self.current_tab == "pdf":
            files = filedialog.askopenfilenames(
                title="Select PDF files to merge",
                filetypes=[("PDF files", "*.pdf")]
            )
            current_list = self.pdf_files
        else:
            files = filedialog.askopenfilenames(
                title="Select Excel files to merge",
                filetypes=[("Excel files", "*.xlsx"), ("Excel files", "*.xls")]
            )
            current_list = self.excel_files
        
        # Add new files
        for file_path in files:
            if file_path not in current_list:
                current_list.append(file_path)
        
        self.update_file_display()
        self.save_session()

    def update_file_display(self):
        # Clear existing file widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        current_files = self.pdf_files if self.current_tab == "pdf" else self.excel_files
        
        # Update header
        file_count = len(current_files)
        file_type = "PDF" if self.current_tab == "pdf" else "Excel"
        self.files_title.configure(text=f"Selected {file_type} Files ({file_count})")
        
        if not current_files:
            # Show empty state
            empty_frame = ttk.Frame(self.scrollable_frame, style='Dark.TFrame')
            empty_frame.pack(fill='x', pady=20)
            
            empty_label = tk.Label(empty_frame, 
                                  text=f"No {file_type.lower()} files selected yet",
                                  font=('Segoe UI', 12),
                                  bg='#1a1a1a', fg='#a1a1aa')
            empty_label.pack()
            
            self.info_label.configure(text="No files selected")
            return
        
        # Display files
        total_size = 0
        for i, file_path in enumerate(current_files):
            self.create_file_item(file_path, i)
            total_size += os.path.getsize(file_path)
        
        # Update info
        size_mb = total_size / (1024 * 1024)
        self.info_label.configure(text=f"{file_count} files • {size_mb:.1f} MB total")

    def create_file_item(self, file_path, index):
        # File item container
        item_frame = tk.Frame(self.scrollable_frame, bg='#2d2d2d', relief='flat', bd=1)
        item_frame.pack(fill='x', pady=2, padx=5)
        
        # File content
        content_frame = tk.Frame(item_frame, bg='#2d2d2d')
        content_frame.pack(fill='x', padx=15, pady=12)
        
        # File icon
        icon = "📄" if self.current_tab == "pdf" else "📊"
        icon_label = tk.Label(content_frame, text=icon, font=('Arial', 20),
                             bg='#2d2d2d', fg='#3b82f6')
        icon_label.pack(side='left', padx=(0, 15))
        
        # File info
        info_frame = tk.Frame(content_frame, bg='#2d2d2d')
        info_frame.pack(side='left', fill='x', expand=True)
        
        # File name
        name_label = tk.Label(info_frame, text=os.path.basename(file_path),
                             font=('Segoe UI', 11, 'bold'),
                             bg='#2d2d2d', fg='#ffffff', anchor='w')
        name_label.pack(fill='x')
        
        # File path and size
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        detail_text = f"{os.path.dirname(file_path)} • {size_mb:.1f} MB"
        detail_label = tk.Label(info_frame, text=detail_text,
                               font=('Segoe UI', 9),
                               bg='#2d2d2d', fg='#a1a1aa', anchor='w')
        detail_label.pack(fill='x')
        
        # Remove button
        remove_btn = tk.Button(content_frame, text="✕", font=('Arial', 12, 'bold'),
                              bg='#2d2d2d', fg='#ef4444', bd=0,
                              cursor='hand2', activebackground='#ef4444',
                              activeforeground='white',
                              command=lambda: self.remove_file(index))
        remove_btn.pack(side='right', padx=(10, 0))

    def remove_file(self, index):
        current_files = self.pdf_files if self.current_tab == "pdf" else self.excel_files
        if 0 <= index < len(current_files):
            del current_files[index]
            self.update_file_display()
            self.save_session()

    def clear_all_files(self):
        if self.current_tab == "pdf":
            self.pdf_files.clear()
        else:
            self.excel_files.clear()
        self.update_file_display()
        self.save_session()

    def show_progress(self, text="Processing...", value=0):
        self.progress_frame.pack(fill='x', pady=(0, 20))
        self.progress_label.configure(text=text)
        self.progress_bar.configure(mode='determinate', value=value)
        self.root.update()

    def hide_progress(self):
        self.progress_frame.pack_forget()

    def merge_files(self):
        current_files = self.pdf_files if self.current_tab == "pdf" else self.excel_files
        
        if not current_files:
            messagebox.showwarning("No Files", f"Please select {self.current_tab.upper()} files to merge.")
            return
        
        # Get output path
        file_type = "PDF" if self.current_tab == "pdf" else "Excel"
        ext = ".pdf" if self.current_tab == "pdf" else ".xlsx"
        
        output_path = filedialog.asksaveasfilename(
            title=f"Save merged {file_type} file",
            defaultextension=ext,
            filetypes=[(f"{file_type} file", f"*{ext}")]
        )
        
        if not output_path:
            return
        
        try:
            if self.current_tab == "pdf":
                self.merge_pdfs(current_files, output_path)
            else:
                self.merge_excels(current_files, output_path)
        except Exception as e:
            self.hide_progress()
            messagebox.showerror("Error", f"Failed to merge files:\n{str(e)}")

    def merge_pdfs(self, files, output_path):
        total_files = len(files)
        merger = PdfMerger()
        
        try:
            for i, pdf_path in enumerate(files):
                progress = int((i / total_files) * 90)
                self.show_progress(f"Processing {os.path.basename(pdf_path)}...", progress)
                merger.append(pdf_path)
            
            self.show_progress("Saving merged PDF...", 95)
            merger.write(output_path)
            merger.close()
            
            self.show_progress("Complete!", 100)
            self.root.after(1000, self.hide_progress)
            
            messagebox.showinfo("Success", f"Successfully merged {total_files} PDF files!\n\nSaved to: {output_path}")
            
        except Exception as e:
            merger.close()
            raise e

    def merge_excels(self, files, output_path):
        total_files = len(files)
        all_data = []
        
        try:
            for i, excel_path in enumerate(files):
                progress = int((i / total_files) * 80)
                self.show_progress(f"Reading {os.path.basename(excel_path)}...", progress)
                
                df = pd.read_excel(excel_path)
                df['Source_File'] = os.path.basename(excel_path)
                all_data.append(df)
            
            self.show_progress("Combining data...", 90)
            combined_df = pd.concat(all_data, ignore_index=True)
            
            self.show_progress("Saving merged Excel file...", 95)
            combined_df.to_excel(output_path, index=False)
            
            self.show_progress("Complete!", 100)
            self.root.after(1000, self.hide_progress)
            
            messagebox.showinfo("Success", f"Successfully merged {total_files} Excel files!\n\nSaved to: {output_path}")
            
        except Exception as e:
            raise e

    def save_session(self):
        data = {
            "pdf_files": self.pdf_files,
            "excel_files": self.excel_files,
            "current_tab": self.current_tab
        }
        try:
            with open(SESSION_FILE, "w") as f:
                json.dump(data, f)
        except Exception as e:
            print("Could not save session:", e)

    def load_session(self):
        if os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, "r") as f:
                    data = json.load(f)
                    self.pdf_files = data.get("pdf_files", [])
                    self.excel_files = data.get("excel_files", [])
                    self.current_tab = data.get("current_tab", "pdf")
                    self.switch_tab(self.current_tab)
            except Exception as e:
                print("Could not load session:", e)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ModernFileManager(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()