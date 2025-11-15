#!/usr/bin/env python3
"""
Mother of Hydra - Advanced Password Attack Interface
A dark-themed GUI wrapper for the Hydra password cracker
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import subprocess
import threading
import os
import queue
from datetime import datetime

class HackerStyle:
    """Dark hacker theme colors and styles"""
    BG_DARK = "#0a0e27"
    BG_MEDIUM = "#16213e"
    BG_LIGHT = "#1a2332"
    FG_PRIMARY = "#00ff41"  # Matrix green
    FG_SECONDARY = "#0dff92"
    FG_ACCENT = "#ff00ff"  # Magenta
    FG_WARNING = "#ff0055"
    FG_INFO = "#00d4ff"
    FG_TEXT = "#c5c6c7"
    BORDER = "#00ff41"
    
    @staticmethod
    def configure_style():
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('.',
                       background=HackerStyle.BG_DARK,
                       foreground=HackerStyle.FG_TEXT,
                       fieldbackground=HackerStyle.BG_MEDIUM,
                       bordercolor=HackerStyle.BORDER,
                       focuscolor=HackerStyle.FG_PRIMARY)
        
        # Frame
        style.configure('TFrame',
                       background=HackerStyle.BG_DARK,
                       borderwidth=1)
        
        # LabelFrame
        style.configure('TLabelframe',
                       background=HackerStyle.BG_DARK,
                       foreground=HackerStyle.FG_PRIMARY,
                       bordercolor=HackerStyle.FG_PRIMARY,
                       borderwidth=2)
        style.configure('TLabelframe.Label',
                       background=HackerStyle.BG_DARK,
                       foreground=HackerStyle.FG_PRIMARY,
                       font=('Consolas', 10, 'bold'))
        
        # Label
        style.configure('TLabel',
                       background=HackerStyle.BG_DARK,
                       foreground=HackerStyle.FG_TEXT,
                       font=('Consolas', 9))
        
        style.configure('Title.TLabel',
                       foreground=HackerStyle.FG_PRIMARY,
                       font=('Consolas', 16, 'bold'))
        
        style.configure('Subtitle.TLabel',
                       foreground=HackerStyle.FG_SECONDARY,
                       font=('Consolas', 8))
        
        # Entry
        style.configure('TEntry',
                       fieldbackground=HackerStyle.BG_MEDIUM,
                       foreground=HackerStyle.FG_TEXT,
                       bordercolor=HackerStyle.FG_PRIMARY,
                       insertcolor=HackerStyle.FG_PRIMARY,
                       font=('Consolas', 9))
        
        # Button
        style.configure('TButton',
                       background=HackerStyle.BG_MEDIUM,
                       foreground=HackerStyle.FG_PRIMARY,
                       bordercolor=HackerStyle.FG_PRIMARY,
                       font=('Consolas', 9, 'bold'),
                       focuscolor=HackerStyle.FG_ACCENT)
        
        style.map('TButton',
                 background=[('active', HackerStyle.BG_LIGHT),
                           ('pressed', HackerStyle.FG_PRIMARY)],
                 foreground=[('active', HackerStyle.FG_SECONDARY)])
        
        # Attack button (special style)
        style.configure('Attack.TButton',
                       background=HackerStyle.BG_MEDIUM,
                       foreground=HackerStyle.FG_WARNING,
                       bordercolor=HackerStyle.FG_WARNING,
                       font=('Consolas', 10, 'bold'))
        
        style.map('Attack.TButton',
                 background=[('active', HackerStyle.FG_WARNING),
                           ('pressed', HackerStyle.FG_PRIMARY)],
                 foreground=[('active', HackerStyle.BG_DARK)])
        
        # Stop button
        style.configure('Stop.TButton',
                       background=HackerStyle.BG_MEDIUM,
                       foreground=HackerStyle.FG_ACCENT,
                       bordercolor=HackerStyle.FG_ACCENT)
        
        # Radiobutton
        style.configure('TRadiobutton',
                       background=HackerStyle.BG_DARK,
                       foreground=HackerStyle.FG_TEXT,
                       font=('Consolas', 8))
        
        # Checkbutton
        style.configure('TCheckbutton',
                       background=HackerStyle.BG_DARK,
                       foreground=HackerStyle.FG_TEXT,
                       font=('Consolas', 8))


class MotherOfHydra:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ MOTHER OF HYDRA ⚡")
        self.root.geometry("1200x1000")
        self.root.configure(bg=HackerStyle.BG_DARK)
        
        # Configure style
        HackerStyle.configure_style()
        
        # Process management
        self.process = None
        self.output_queue = queue.Queue()
        self.attack_start_time = None
        
        # ASCII Art Header
        self.create_header()
        
        # Create main container with scrollbar
        canvas = tk.Canvas(root, bg=HackerStyle.BG_DARK, highlightthickness=0)
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
        
        self.main_frame = ttk.Frame(canvas)
        self.main_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Build interface
        self.create_interface()
        
        # Start time ticker
        self.update_time()
        
    def create_header(self):
        """Create ASCII art header"""
        header_frame = tk.Frame(self.root, bg=HackerStyle.BG_DARK)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ascii_art = """
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   ███╗   ███╗ ██████╗ ████████╗██╗  ██╗███████╗██████╗                   ║
║   ████╗ ████║██╔═══██╗╚══██╔══╝██║  ██║██╔════╝██╔══██╗                  ║
║   ██╔████╔██║██║   ██║   ██║   ███████║█████╗  ██████╔╝                  ║
║   ██║╚██╔╝██║██║   ██║   ██║   ██╔══██║██╔══╝  ██╔══██╗                  ║
║   ██║ ╚═╝ ██║╚██████╔╝   ██║   ██║  ██║███████╗██║  ██║                  ║
║   ╚═╝     ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝                  ║
║                                                                           ║
║           ██████╗ ███████╗    ██╗  ██╗██╗   ██╗██████╗ ██████╗  █████╗  ║
║          ██╔═══██╗██╔════╝    ██║  ██║╚██╗ ██╔╝██╔══██╗██╔══██╗██╔══██╗ ║
║          ██║   ██║█████╗      ███████║ ╚████╔╝ ██║  ██║██████╔╝███████║ ║
║          ██║   ██║██╔══╝      ██╔══██║  ╚██╔╝  ██║  ██║██╔══██╗██╔══██║ ║
║          ╚██████╔╝██║         ██║  ██║   ██║   ██████╔╝██║  ██║██║  ██║ ║
║           ╚═════╝ ╚═╝         ╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ║
║                                                                           ║
║              ═══[ Advanced Password Attack Framework ]═══                ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
        """
        
        ascii_label = tk.Label(
            header_frame,
            text=ascii_art,
            font=('Courier', 7),
            fg=HackerStyle.FG_PRIMARY,
            bg=HackerStyle.BG_DARK,
            justify=tk.LEFT
        )
        ascii_label.pack()
        
        # System time
        self.time_label = tk.Label(
            header_frame,
            text="",
            font=('Consolas', 9),
            fg=HackerStyle.FG_SECONDARY,
            bg=HackerStyle.BG_DARK
        )
        self.time_label.pack()
        
    def update_time(self):
        """Update system time display"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=f"⚡ SYSTEM TIME: {current_time} ⚡")
        self.root.after(1000, self.update_time)
    
    def create_interface(self):
        """Build the main interface"""
        
        # Attack Type Selection
        attack_frame = ttk.LabelFrame(self.main_frame, text="⚔ ATTACK VECTOR ⚔", padding="10")
        attack_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.attack_type = tk.StringVar(value="http-post-form")
        
        attacks = [
            ("🌐 HTTP POST", "http-post-form"),
            ("🔒 HTTPS POST", "https-post-form"),
            ("🌐 HTTP GET", "http-get-form"),
            ("🔒 HTTPS GET", "https-get-form"),
            ("🔑 SSH", "ssh"),
            ("📁 FTP", "ftp"),
            ("📡 TELNET", "telnet"),
            ("🖥 SMB", "smb"),
            ("🖥 RDP", "rdp")
        ]
        
        attack_grid = tk.Frame(attack_frame, bg=HackerStyle.BG_DARK)
        attack_grid.pack(fill=tk.X)
        
        for i, (text, value) in enumerate(attacks):
            rb = ttk.Radiobutton(
                attack_grid,
                text=text,
                variable=self.attack_type,
                value=value,
                command=self.toggle_form_options
            )
            rb.grid(row=i//3, column=i%3, sticky=tk.W, padx=10, pady=3)
        
        # Target Configuration
        target_frame = ttk.LabelFrame(self.main_frame, text="🎯 TARGET CONFIGURATION 🎯", padding="10")
        target_frame.pack(fill=tk.X, padx=5, pady=5)
        
        target_grid = tk.Frame(target_frame, bg=HackerStyle.BG_DARK)
        target_grid.pack(fill=tk.X)
        target_grid.columnconfigure(1, weight=1)
        
        ttk.Label(target_grid, text="🎯 Target Host:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.target = tk.StringVar()
        target_entry = ttk.Entry(target_grid, textvariable=self.target, width=50)
        target_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        ttk.Label(target_grid, text="🔌 Port:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.port = tk.StringVar()
        ttk.Entry(target_grid, textvariable=self.port, width=20).grid(
            row=1, column=1, sticky=tk.W, pady=5, padx=5)
        
        # HTTP/HTTPS Form Options
        self.form_frame = ttk.LabelFrame(
            self.main_frame,
            text="🌐 HTTP/HTTPS FORM PARAMETERS 🌐",
            padding="10"
        )
        self.form_frame.pack(fill=tk.X, padx=5, pady=5)
        
        form_grid = tk.Frame(self.form_frame, bg=HackerStyle.BG_DARK)
        form_grid.pack(fill=tk.X)
        form_grid.columnconfigure(1, weight=1)
        
        ttk.Label(form_grid, text="📄 Form Path:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.form_path = tk.StringVar(value="/login")
        ttk.Entry(form_grid, textvariable=self.form_path, width=50).grid(
            row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        ttk.Label(form_grid, text="⚙ Parameters:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.form_params = tk.StringVar(value="username=^USER^&password=^PASS^")
        ttk.Entry(form_grid, textvariable=self.form_params, width=50).grid(
            row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        hint = tk.Label(
            form_grid,
            text="💡 Use ^USER^ and ^PASS^ as placeholders",
            font=('Consolas', 8, 'italic'),
            fg=HackerStyle.FG_SECONDARY,
            bg=HackerStyle.BG_DARK
        )
        hint.grid(row=2, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(form_grid, text="❌ Failure String:").grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        self.failure_string = tk.StringVar(value="Login failed")
        ttk.Entry(form_grid, textvariable=self.failure_string, width=50).grid(
            row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        ttk.Label(form_grid, text="✓ Success String:").grid(row=4, column=0, sticky=tk.W, pady=5, padx=5)
        self.success_string = tk.StringVar()
        ttk.Entry(form_grid, textvariable=self.success_string, width=50).grid(
            row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        ttk.Label(form_grid, text="📋 Headers:").grid(row=5, column=0, sticky=tk.W, pady=5, padx=5)
        self.headers = tk.StringVar()
        ttk.Entry(form_grid, textvariable=self.headers, width=50).grid(
            row=5, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Credentials
        creds_frame = ttk.LabelFrame(self.main_frame, text="🔐 CREDENTIALS PAYLOAD 🔐", padding="10")
        creds_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Username section
        user_section = tk.Frame(creds_frame, bg=HackerStyle.BG_DARK)
        user_section.pack(fill=tk.X, pady=5)
        
        tk.Label(
            user_section,
            text="👤 USERNAME:",
            font=('Consolas', 9, 'bold'),
            fg=HackerStyle.FG_PRIMARY,
            bg=HackerStyle.BG_DARK
        ).pack(anchor=tk.W)
        
        self.username_mode = tk.StringVar(value="single")
        
        user_single = tk.Frame(user_section, bg=HackerStyle.BG_DARK)
        user_single.pack(fill=tk.X, pady=2)
        ttk.Radiobutton(user_single, text="Single:", variable=self.username_mode, 
                       value="single").pack(side=tk.LEFT)
        self.username = tk.StringVar()
        ttk.Entry(user_single, textvariable=self.username, width=40).pack(side=tk.LEFT, padx=5)
        
        user_list = tk.Frame(user_section, bg=HackerStyle.BG_DARK)
        user_list.pack(fill=tk.X, pady=2)
        ttk.Radiobutton(user_list, text="List:", variable=self.username_mode, 
                       value="list").pack(side=tk.LEFT)
        self.username_list = tk.StringVar()
        ttk.Entry(user_list, textvariable=self.username_list, width=40).pack(side=tk.LEFT, padx=5)
        ttk.Button(user_list, text="📁 Browse", 
                  command=lambda: self.browse_file(self.username_list)).pack(side=tk.LEFT, padx=5)
        
        # Password section
        pass_section = tk.Frame(creds_frame, bg=HackerStyle.BG_DARK)
        pass_section.pack(fill=tk.X, pady=5)
        
        tk.Label(
            pass_section,
            text="🔑 PASSWORD:",
            font=('Consolas', 9, 'bold'),
            fg=HackerStyle.FG_PRIMARY,
            bg=HackerStyle.BG_DARK
        ).pack(anchor=tk.W)
        
        self.password_mode = tk.StringVar(value="list")
        
        pass_single = tk.Frame(pass_section, bg=HackerStyle.BG_DARK)
        pass_single.pack(fill=tk.X, pady=2)
        ttk.Radiobutton(pass_single, text="Single:", variable=self.password_mode, 
                       value="single").pack(side=tk.LEFT)
        self.password = tk.StringVar()
        pass_entry = ttk.Entry(pass_single, textvariable=self.password, width=40, show="*")
        pass_entry.pack(side=tk.LEFT, padx=5)
        
        pass_list = tk.Frame(pass_section, bg=HackerStyle.BG_DARK)
        pass_list.pack(fill=tk.X, pady=2)
        ttk.Radiobutton(pass_list, text="List:", variable=self.password_mode, 
                       value="list").pack(side=tk.LEFT)
        self.password_list = tk.StringVar()
        ttk.Entry(pass_list, textvariable=self.password_list, width=40).pack(side=tk.LEFT, padx=5)
        ttk.Button(pass_list, text="📁 Browse", 
                  command=lambda: self.browse_file(self.password_list)).pack(side=tk.LEFT, padx=5)
        
        # Advanced Options
        adv_frame = ttk.LabelFrame(self.main_frame, text="⚙ ADVANCED OPTIONS ⚙", padding="10")
        adv_frame.pack(fill=tk.X, padx=5, pady=5)
        
        options_grid = tk.Frame(adv_frame, bg=HackerStyle.BG_DARK)
        options_grid.pack(fill=tk.X)
        
        ttk.Label(options_grid, text="🧵 Threads:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.threads = tk.StringVar(value="16")
        ttk.Entry(options_grid, textvariable=self.threads, width=10).grid(
            row=0, column=1, sticky=tk.W, pady=5, padx=5)
        
        ttk.Label(options_grid, text="⏱ Timeout:").grid(row=0, column=2, sticky=tk.W, pady=5, padx=15)
        self.timeout = tk.StringVar(value="30")
        ttk.Entry(options_grid, textvariable=self.timeout, width=10).grid(
            row=0, column=3, sticky=tk.W, pady=5, padx=5)
        
        self.verbose = tk.BooleanVar()
        ttk.Checkbutton(options_grid, text="📢 Verbose", variable=self.verbose).grid(
            row=1, column=0, columnspan=2, sticky=tk.W, pady=5, padx=5)
        
        self.show_attempts = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_grid, text="👁 Show Attempts", variable=self.show_attempts).grid(
            row=1, column=2, columnspan=2, sticky=tk.W, pady=5, padx=5)
        
        # Statistics Display
        stats_frame = ttk.LabelFrame(self.main_frame, text="📊 ATTACK STATISTICS 📊", padding="10")
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        stats_grid = tk.Frame(stats_frame, bg=HackerStyle.BG_DARK)
        stats_grid.pack(fill=tk.X)
        
        self.stats_labels = {}
        stats = [
            ("⏱ Elapsed:", "00:00:00"),
            ("🎯 Attempts:", "0"),
            ("✓ Valid:", "0"),
            ("⚡ Speed:", "0/s")
        ]
        
        for i, (label, value) in enumerate(stats):
            tk.Label(
                stats_grid,
                text=label,
                font=('Consolas', 9, 'bold'),
                fg=HackerStyle.FG_SECONDARY,
                bg=HackerStyle.BG_DARK
            ).grid(row=0, column=i*2, sticky=tk.W, padx=5)
            
            stat_label = tk.Label(
                stats_grid,
                text=value,
                font=('Consolas', 9),
                fg=HackerStyle.FG_PRIMARY,
                bg=HackerStyle.BG_DARK
            )
            stat_label.grid(row=0, column=i*2+1, sticky=tk.W, padx=5)
            self.stats_labels[label] = stat_label
        
        # Control Buttons
        button_frame = tk.Frame(self.main_frame, bg=HackerStyle.BG_DARK)
        button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        self.start_button = ttk.Button(
            button_frame,
            text="⚡ INITIATE ATTACK ⚡",
            command=self.start_attack,
            style='Attack.TButton'
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(
            button_frame,
            text="⛔ TERMINATE ⛔",
            command=self.stop_attack,
            style='Stop.TButton',
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="🗑 Clear",
            command=self.clear_output
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="💾 Save Log",
            command=self.save_output
        ).pack(side=tk.LEFT, padx=5)
        
        # Output
        output_frame = ttk.LabelFrame(self.main_frame, text="💻 SYSTEM OUTPUT 💻", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            height=20,
            width=100,
            bg=HackerStyle.BG_MEDIUM,
            fg=HackerStyle.FG_TEXT,
            insertbackground=HackerStyle.FG_PRIMARY,
            font=('Consolas', 9),
            borderwidth=2,
            relief=tk.SUNKEN
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for colored output
        self.output_text.tag_config("success", foreground=HackerStyle.FG_PRIMARY, font=('Consolas', 9, 'bold'))
        self.output_text.tag_config("error", foreground=HackerStyle.FG_WARNING, font=('Consolas', 9, 'bold'))
        self.output_text.tag_config("info", foreground=HackerStyle.FG_INFO)
        self.output_text.tag_config("warning", foreground=HackerStyle.FG_ACCENT)
        
        # Status bar
        status_frame = tk.Frame(self.main_frame, bg=HackerStyle.BG_MEDIUM, relief=tk.SUNKEN, borderwidth=2)
        status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.status_var = tk.StringVar(value="⚡ SYSTEM READY - AWAITING INSTRUCTIONS ⚡")
        tk.Label(
            status_frame,
            textvariable=self.status_var,
            bg=HackerStyle.BG_MEDIUM,
            fg=HackerStyle.FG_PRIMARY,
            font=('Consolas', 9, 'bold'),
            anchor=tk.W,
            padx=10,
            pady=5
        ).pack(fill=tk.X)
        
        # Welcome message
        welcome_msg = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                  MOTHER OF HYDRA - ATTACK FRAMEWORK v1.0                    ║
║                                                                              ║
║  [+] Multi-Protocol Password Attack System                                  ║
║  [+] HTTP/HTTPS Form Authentication Brute Force                             ║
║  [+] SSH/FTP/Telnet/SMB/RDP Protocol Support                                ║
║  [+] Multi-Threaded High-Speed Operations                                   ║
║                                                                              ║
║  WARNING: For authorized penetration testing only!                          ║
║  Unauthorized access to computer systems is illegal.                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

"""
        self.output_text.insert(tk.END, welcome_msg, "info")
        
        # Initialize form options visibility
        self.toggle_form_options()
        
    def toggle_form_options(self):
        """Show/hide form options based on attack type"""
        attack = self.attack_type.get()
        if 'http' in attack or 'https' in attack:
            self.form_frame.pack(fill=tk.X, padx=5, pady=5, 
                               before=self.main_frame.winfo_children()[3])
        else:
            self.form_frame.pack_forget()
    
    def browse_file(self, var):
        """Browse for a file and set the variable"""
        filename = filedialog.askopenfilename(
            title="Select File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            var.set(filename)
    
    def validate_inputs(self):
        """Validate all inputs before starting attack"""
        if not self.target.get():
            self.show_error("TARGET REQUIRED", "Please specify a target host")
            return False
        
        # Check username
        if self.username_mode.get() == "single":
            if not self.username.get():
                self.show_error("USERNAME REQUIRED", "Please specify a username")
                return False
        else:
            if not self.username_list.get() or not os.path.exists(self.username_list.get()):
                self.show_error("INVALID USERNAME LIST", "Please specify a valid username list file")
                return False
        
        # Check password
        if self.password_mode.get() == "single":
            if not self.password.get():
                self.show_error("PASSWORD REQUIRED", "Please specify a password")
                return False
        else:
            if not self.password_list.get() or not os.path.exists(self.password_list.get()):
                self.show_error("INVALID PASSWORD LIST", "Please specify a valid password list file")
                return False
        
        # Check if hydra is installed
        try:
            subprocess.run(['hydra', '-h'], capture_output=True, timeout=5)
        except FileNotFoundError:
            self.show_error("HYDRA NOT FOUND", "Hydra is not installed or not in PATH")
            return False
        except Exception as e:
            self.show_error("HYDRA ERROR", f"Error checking Hydra: {str(e)}")
            return False
        
        return True
    
    def show_error(self, title, message):
        """Show custom error dialog"""
        error_window = tk.Toplevel(self.root)
        error_window.title(f"❌ {title}")
        error_window.configure(bg=HackerStyle.BG_DARK)
        error_window.geometry("400x150")
        
        tk.Label(
            error_window,
            text=f"⚠ {title} ⚠",
            font=('Consolas', 12, 'bold'),
            fg=HackerStyle.FG_WARNING,
            bg=HackerStyle.BG_DARK
        ).pack(pady=10)
        
        tk.Label(
            error_window,
            text=message,
            font=('Consolas', 9),
            fg=HackerStyle.FG_TEXT,
            bg=HackerStyle.BG_DARK,
            wraplength=350
        ).pack(pady=10)
        
        ttk.Button(
            error_window,
            text="OK",
            command=error_window.destroy
        ).pack(pady=10)
        
    def build_command(self):
        """Build the Hydra command based on GUI inputs"""
        cmd = ['hydra']
        
        # Username
        if self.username_mode.get() == "single":
            cmd.extend(['-l', self.username.get()])
        else:
            cmd.extend(['-L', self.username_list.get()])
        
        # Password
        if self.password_mode.get() == "single":
            cmd.extend(['-p', self.password.get()])
        else:
            cmd.extend(['-P', self.password_list.get()])
        
        # Threads
        cmd.extend(['-t', self.threads.get()])
        
        # Timeout
        cmd.extend(['-w', self.timeout.get()])
        
        # Verbose
        if self.verbose.get():
            cmd.append('-V')
        elif self.show_attempts.get():
            cmd.append('-v')
        
        # Target and port
        target = self.target.get()
        if self.port.get():
            cmd.extend(['-s', self.port.get()])
        
        cmd.append(target)
        
        # Service/Attack type
        attack = self.attack_type.get()
        
        if 'form' in attack:
            # Build form string
            form_string = f"{self.form_path.get()}:{self.form_params.get()}"
            
            # Add failure or success condition
            if self.success_string.get():
                form_string += f":S={self.success_string.get()}"
            else:
                form_string += f":F={self.failure_string.get()}"
            
            # Add headers if specified
            if self.headers.get():
                form_string += f":H={self.headers.get()}"
            
            cmd.append(attack)
            cmd.append(form_string)
        else:
            cmd.append(attack)
        
        return cmd
    
    def start_attack(self):
        """Start the Hydra attack"""
        if not self.validate_inputs():
            return
        
        cmd = self.build_command()
        
        # Display command
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.output_text.insert(tk.END, f"\n{'='*80}\n", "info")
        self.output_text.insert(tk.END, f"[{timestamp}] INITIATING ATTACK\n", "warning")
        self.output_text.insert(tk.END, f"{'='*80}\n", "info")
        self.output_text.insert(tk.END, f"COMMAND: {' '.join(cmd)}\n\n", "info")
        self.output_text.see(tk.END)
        
        # Reset statistics
        self.attack_start_time = datetime.now()
        self.stats_labels["⏱ Elapsed:"].config(text="00:00:00")
        self.stats_labels["🎯 Attempts:"].config(text="0")
        self.stats_labels["✓ Valid:"].config(text="0")
        self.stats_labels["⚡ Speed:"].config(text="0/s")
        
        # Update UI
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_var.set("⚡ ATTACK IN PROGRESS - BREACHING DEFENSES ⚡")
        
        # Start attack in separate thread
        thread = threading.Thread(target=self.run_attack, args=(cmd,), daemon=True)
        thread.start()
        
        # Start output monitoring
        self.root.after(100, self.check_output)
        self.root.after(1000, self.update_stats)
    
    def run_attack(self, cmd):
        """Run the Hydra attack in a separate thread"""
        try:
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Read output line by line
            for line in self.process.stdout:
                self.output_queue.put(('output', line))
            
            # Wait for process to complete
            self.process.wait()
            
            if self.process.returncode == 0:
                self.output_queue.put(('status', '✓ ATTACK COMPLETED SUCCESSFULLY'))
            else:
                self.output_queue.put(('status', f'⚠ ATTACK TERMINATED - CODE {self.process.returncode}'))
                
        except Exception as e:
            self.output_queue.put(('error', str(e)))
        finally:
            self.output_queue.put(('done', None))
    
    def check_output(self):
        """Check for new output from the attack thread"""
        try:
            while True:
                msg_type, msg = self.output_queue.get_nowait()
                
                if msg_type == 'output':
                    # Determine tag based on content
                    tag = None
                    if 'valid password' in msg.lower() or '[' in msg and ']' in msg and 'host:' in msg.lower():
                        tag = "success"
                        self.output_text.insert(tk.END, "✓ ", "success")
                    elif 'error' in msg.lower():
                        tag = "error"
                        self.output_text.insert(tk.END, "❌ ", "error")
                    elif 'attempt' in msg.lower():
                        tag = "info"
                    
                    self.output_text.insert(tk.END, msg, tag)
                    self.output_text.see(tk.END)
                
                elif msg_type == 'status':
                    self.status_var.set(msg)
                    self.output_text.insert(tk.END, f"\n{'='*80}\n", "info")
                    self.output_text.insert(tk.END, f"{msg}\n", "warning")
                    self.output_text.insert(tk.END, f"{'='*80}\n\n", "info")
                    self.output_text.see(tk.END)
                
                elif msg_type == 'error':
                    self.status_var.set(f"❌ ERROR: {msg}")
                    self.output_text.insert(tk.END, f"\n❌ ERROR: {msg}\n", "error")
                    self.output_text.see(tk.END)
                    self.show_error("ATTACK ERROR", msg)
                
                elif msg_type == 'done':
                    self.start_button.config(state=tk.NORMAL)
                    self.stop_button.config(state=tk.DISABLED)
                    self.process = None
                    self.attack_start_time = None
                    return
                    
        except queue.Empty:
            pass
        
        # Schedule next check
        if self.process is not None:
            self.root.after(100, self.check_output)
    
    def update_stats(self):
        """Update attack statistics"""
        if self.attack_start_time:
            elapsed = datetime.now() - self.attack_start_time
            hours, remainder = divmod(elapsed.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.stats_labels["⏱ Elapsed:"].config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            
            # Schedule next update
            self.root.after(1000, self.update_stats)
    
    def stop_attack(self):
        """Stop the running attack"""
        if self.process:
            self.process.terminate()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.output_text.insert(tk.END, f"\n{'='*80}\n", "info")
            self.output_text.insert(tk.END, f"[{timestamp}] ⛔ ATTACK TERMINATED BY USER\n", "warning")
            self.output_text.insert(tk.END, f"{'='*80}\n\n", "info")
            self.output_text.see(tk.END)
            self.status_var.set("⛔ ATTACK TERMINATED - SYSTEM IDLE ⛔")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.process = None
            self.attack_start_time = None
    
    def clear_output(self):
        """Clear the output text"""
        self.output_text.delete(1.0, tk.END)
        self.status_var.set("⚡ OUTPUT CLEARED - SYSTEM READY ⚡")
    
    def save_output(self):
        """Save the output to a file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = filedialog.asksaveasfilename(
            title="Save Attack Log",
            defaultextension=".txt",
            initialfile=f"hydra_attack_{timestamp}.txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.output_text.get(1.0, tk.END))
                self.status_var.set(f"💾 LOG SAVED: {filename}")
                
                # Success message
                success_window = tk.Toplevel(self.root)
                success_window.title("✓ SUCCESS")
                success_window.configure(bg=HackerStyle.BG_DARK)
                success_window.geometry("350x120")
                
                tk.Label(
                    success_window,
                    text="✓ LOG SAVED SUCCESSFULLY",
                    font=('Consolas', 11, 'bold'),
                    fg=HackerStyle.FG_PRIMARY,
                    bg=HackerStyle.BG_DARK
                ).pack(pady=10)
                
                tk.Label(
                    success_window,
                    text=filename,
                    font=('Consolas', 8),
                    fg=HackerStyle.FG_TEXT,
                    bg=HackerStyle.BG_DARK,
                    wraplength=300
                ).pack(pady=5)
                
                ttk.Button(
                    success_window,
                    text="OK",
                    command=success_window.destroy
                ).pack(pady=10)
                
            except Exception as e:
                self.show_error("SAVE ERROR", f"Failed to save output: {str(e)}")


def main():
    # Check if running as root (required for some Hydra operations)
    if os.name != 'nt' and os.geteuid() != 0:
        print("⚠ WARNING: Some features may require root privileges")
    
    root = tk.Tk()
    
    # Set window icon (if you have one)
    # root.iconbitmap('icon.ico')
    
    app = MotherOfHydra(root)
    root.mainloop()


if __name__ == "__main__":
    main()

