import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip  # For clipboard functionality (install: pip install pyperclip)

# Global variables to store GUI elements
root = None
length_var = None
uppercase_var = None
lowercase_var = None
numbers_var = None
symbols_var = None
password_var = None
strength_var = None
strength_progress = None

def initialize_gui():
    """Initialize the main GUI window and all variables"""
    global root, length_var, uppercase_var, lowercase_var, numbers_var, symbols_var, password_var, strength_var, strength_progress
    
    # Create main window
    root = tk.Tk()
    root.title("🔐 Password Generator")
    root.geometry("600x750")
    root.configure(bg='#f0f2f5')
    root.resizable(False, False)
    
    # Initialize variables
    length_var = tk.IntVar(value=12)
    uppercase_var = tk.BooleanVar(value=True)
    lowercase_var = tk.BooleanVar(value=True)
    numbers_var = tk.BooleanVar(value=True)
    symbols_var = tk.BooleanVar(value=True)
    password_var = tk.StringVar()
    strength_var = tk.StringVar(value="Password strength will appear here")

def create_title():
    """Create the application title"""
    title_frame = tk.Frame(root, bg='#f0f2f5')
    title_frame.pack(pady=20)
    
    title_label = tk.Label(
        title_frame,
        text="🔐 Password Generator",
        font=('Arial', 24, 'bold'),
        bg='#f0f2f5',
        fg='#2c3e50'
    )
    title_label.pack()
    
    subtitle_label = tk.Label(
        title_frame,
        text="Generate secure passwords with custom criteria",
        font=('Arial', 12),
        bg='#f0f2f5',
        fg='#7f8c8d'
    )
    subtitle_label.pack(pady=(5, 0))

def create_length_section():
    """Create the password length input section"""
    length_frame = tk.LabelFrame(
        root,
        text="Password Length",
        font=('Arial', 12, 'bold'),
        bg='#f0f2f5',
        fg='#2c3e50',
        padx=20,
        pady=15
    )
    length_frame.pack(pady=10, padx=30, fill='x')
    
    # Length slider
    length_scale = tk.Scale(
        length_frame,
        from_=4,
        to=50,
        orient='horizontal',
        variable=length_var,
        font=('Arial', 10),
        bg='#f0f2f5',
        fg='#2c3e50',
        activebackground='#3498db',
        highlightthickness=0,
        troughcolor='#ecf0f1',
        command=lambda x: update_password_display()
    )
    length_scale.pack(fill='x', pady=(0, 10))
    
    # Length display
    length_display = tk.Label(
        length_frame,
        textvariable=length_var,
        font=('Arial', 14, 'bold'),
        bg='#f0f2f5',
        fg='#e74c3c'
    )
    length_display.pack()

def create_options_section():
    """Create the character type selection section"""
    options_frame = tk.LabelFrame(
        root,
        text="Character Types",
        font=('Arial', 12, 'bold'),
        bg='#f0f2f5',
        fg='#2c3e50',
        padx=20,
        pady=15
    )
    options_frame.pack(pady=10, padx=30, fill='x')
    
    # Checkbox options
    options = [
        ("Uppercase Letters (A-Z)", uppercase_var, "ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        ("Lowercase Letters (a-z)", lowercase_var, "abcdefghijklmnopqrstuvwxyz"),
        ("Numbers (0-9)", numbers_var, "0123456789"),
        ("Special Characters (!@#$)", symbols_var, "!@#$%^&*()_+-=[]{}|;:,.<>?")
    ]
    
    for text, var, example in options:
        checkbox_frame = tk.Frame(options_frame, bg='#f0f2f5')
        checkbox_frame.pack(fill='x', pady=5)
        
        checkbox = tk.Checkbutton(
            checkbox_frame,
            text=text,
            variable=var,
            font=('Arial', 11),
            bg='#f0f2f5',
            fg='#2c3e50',
            activebackground='#f0f2f5',
            selectcolor='#3498db',
            command=update_password_display
        )
        checkbox.pack(side='left')
        
        example_label = tk.Label(
            checkbox_frame,
            text=f"({example[:10]}...)" if len(example) > 10 else f"({example})",
            font=('Arial', 9),
            bg='#f0f2f5',
            fg='#95a5a6'
        )
        example_label.pack(side='right')

def create_buttons_section():
    """Create the action buttons section"""
    buttons_frame = tk.Frame(root, bg='#f0f2f5')
    buttons_frame.pack(pady=20)
    
    # Generate button
    generate_btn = tk.Button(
        buttons_frame,
        text="🎲 Generate Password",
        command=generate_password,
        font=('Arial', 14, 'bold'),
        bg='#3498db',
        fg='white',
        activebackground='#2980b9',
        activeforeground='white',
        relief='flat',
        padx=30,
        pady=12,
        cursor='hand2'
    )
    generate_btn.pack(side='left', padx=10)
    
    # Copy button
    copy_btn = tk.Button(
        buttons_frame,
        text="📋 Copy to Clipboard",
        command=copy_password,
        font=('Arial', 14, 'bold'),
        bg='#27ae60',
        fg='white',
        activebackground='#229954',
        activeforeground='white',
        relief='flat',
        padx=30,
        pady=12,
        cursor='hand2'
    )
    copy_btn.pack(side='left', padx=10)

def create_password_display():
    """Create the password display section"""
    display_frame = tk.LabelFrame(
        root,
        text="Generated Password",
        font=('Arial', 12, 'bold'),
        bg='#f0f2f5',
        fg='#2c3e50',
        padx=20,
        pady=15
    )
    display_frame.pack(pady=10, padx=30, fill='x')
    
    # Password text area
    password_text = tk.Text(
        display_frame,
        height=3,
        font=('Courier New', 12, 'bold'),
        bg='#ecf0f1',
        fg='#2c3e50',
        wrap='word',
        relief='solid',
        bd=1,
        state='disabled'
    )
    password_text.pack(fill='x', pady=(0, 10))
    
    # Store reference for updating
    root.password_text = password_text

def create_strength_indicator():
    """Create the password strength indicator section"""
    strength_frame = tk.LabelFrame(
        root,
        text="Password Strength",
        font=('Arial', 12, 'bold'),
        bg='#f0f2f5',
        fg='#2c3e50',
        padx=20,
        pady=15
    )
    strength_frame.pack(pady=10, padx=30, fill='x')
    
    # Strength progress bar
    global strength_progress
    strength_progress = ttk.Progressbar(
        strength_frame,
        length=400,
        mode='determinate',
        style='Strength.Horizontal.TProgressbar'
    )
    strength_progress.pack(fill='x', pady=(0, 10))
    
    # Strength label
    strength_label = tk.Label(
        strength_frame,
        textvariable=strength_var,
        font=('Arial', 11, 'bold'),
        bg='#f0f2f5',
        fg='#7f8c8d'
    )
    strength_label.pack()

def configure_styles():
    """Configure custom styles for the application"""
    style = ttk.Style()
    
    # Configure progress bar styles
    style.configure(
        'Strength.Horizontal.TProgressbar',
        background='#3498db',
        troughcolor='#ecf0f1',
        borderwidth=0,
        lightcolor='#3498db',
        darkcolor='#3498db'
    )

def get_character_sets():
    """Get the selected character sets based on user choices"""
    char_sets = ""
    
    if uppercase_var.get():
        char_sets += string.ascii_uppercase
    if lowercase_var.get():
        char_sets += string.ascii_lowercase
    if numbers_var.get():
        char_sets += string.digits
    if symbols_var.get():
        char_sets += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    return char_sets

def validate_selection():
    """Validate that at least one character type is selected"""
    if not any([uppercase_var.get(), lowercase_var.get(), numbers_var.get(), symbols_var.get()]):
        messagebox.showerror(
            "Invalid Selection",
            "Please select at least one character type!"
        )
        return False
    return True

def generate_secure_password(length, char_sets):
    """Generate a secure password with guaranteed character diversity"""
    if not char_sets:
        return ""
    
    password = []
    guaranteed_chars = []
    
    # Ensure at least one character from each selected set
    if uppercase_var.get():
        guaranteed_chars.append(random.choice(string.ascii_uppercase))
    if lowercase_var.get():
        guaranteed_chars.append(random.choice(string.ascii_lowercase))
    if numbers_var.get():
        guaranteed_chars.append(random.choice(string.digits))
    if symbols_var.get():
        guaranteed_chars.append(random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
    
    # Add guaranteed characters
    password.extend(guaranteed_chars)
    
    # Fill remaining positions with random characters
    remaining_length = length - len(guaranteed_chars)
    for _ in range(remaining_length):
        password.append(random.choice(char_sets))
    
    # Shuffle to avoid predictable patterns
    random.shuffle(password)
    
    return ''.join(password)

def calculate_password_strength(password):
    """Calculate password strength score (0-100)"""
    if not password:
        return 0
    
    score = 0
    length = len(password)
    
    # Length scoring (0-30 points)
    if length >= 8:
        score += 10
    if length >= 12:
        score += 10
    if length >= 16:
        score += 10
    
    # Character variety scoring (0-40 points)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    variety_score = sum([has_lower, has_upper, has_digit, has_symbol]) * 10
    score += variety_score
    
    # Complexity bonus (0-30 points)
    unique_chars = len(set(password))
    complexity_ratio = unique_chars / length if length > 0 else 0
    score += int(complexity_ratio * 30)
    
    return min(score, 100)

def get_strength_description(score):
    """Get strength description and color based on score"""
    if score < 30:
        return "Very Weak", "#e74c3c"
    elif score < 50:
        return "Weak", "#f39c12"
    elif score < 70:
        return "Moderate", "#f1c40f"
    elif score < 85:
        return "Strong", "#27ae60"
    else:
        return "Very Strong", "#2ecc71"

def update_strength_display(password):
    """Update the password strength indicator"""
    score = calculate_password_strength(password)
    description, color = get_strength_description(score)
    
    # Update progress bar
    strength_progress['value'] = score
    
    # Update strength label
    strength_var.set(f"{description} ({score}/100)")
    
    # Update progress bar color (requires style configuration)
    style = ttk.Style()
    style.configure('Strength.Horizontal.TProgressbar', background=color)

def update_password_display():
    """Update password display when settings change"""
    if hasattr(root, 'password_text') and password_var.get():
        generate_password()

def generate_password():
    """Main function to generate password"""
    if not validate_selection():
        return
    
    length = length_var.get()
    char_sets = get_character_sets()
    
    # Generate password
    password = generate_secure_password(length, char_sets)
    password_var.set(password)
    
    # Update password display
    password_text = root.password_text
    password_text.config(state='normal')
    password_text.delete(1.0, tk.END)
    password_text.insert(1.0, password)
    password_text.config(state='disabled')
    
    # Update strength indicator
    update_strength_display(password)
    
    # Show success message briefly
    original_title = root.title()
    root.title("✅ Password Generated!")
    root.after(2000, lambda: root.title(original_title))

def copy_password():
    """Copy password to clipboard"""
    password = password_var.get()
    if not password:
        messagebox.showwarning("No Password", "Please generate a password first!")
        return
    
    try:
        # Try using pyperclip first
        pyperclip.copy(password)
        messagebox.showinfo("Success", "Password copied to clipboard!")
    except:
        # Fallback to tkinter clipboard
        try:
            root.clipboard_clear()
            root.clipboard_append(password)
            root.update()
            messagebox.showinfo("Success", "Password copied to clipboard!")
        except:
            messagebox.showerror("Error", "Could not copy to clipboard")

def setup_keyboard_shortcuts():
    """Setup keyboard shortcuts for common actions"""
    root.bind('<Control-g>', lambda e: generate_password())
    root.bind('<Control-c>', lambda e: copy_password())
    root.bind('<F5>', lambda e: generate_password())

def create_menu():
    """Create application menu"""
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    # File menu
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Generate Password (Ctrl+G)", command=generate_password)
    file_menu.add_command(label="Copy Password (Ctrl+C)", command=copy_password)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    
    # Help menu
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=show_about)
    help_menu.add_command(label="Keyboard Shortcuts", command=show_shortcuts)

def show_about():
    """Show about dialog"""
    messagebox.showinfo(
        "About Password Generator",
        "Password Generator v1.0\n\n"
        "A secure password generator built with Python and Tkinter.\n\n"
        "Features:\n"
        "• Customizable password length (4-50 characters)\n"
        "• Multiple character type selection\n"
        "• Password strength analysis\n"
        "• One-click clipboard copying\n"
        "• Keyboard shortcuts support\n\n"
        "Created with ❤️ using Python"
    )

def show_shortcuts():
    """Show keyboard shortcuts dialog"""
    messagebox.showinfo(
        "Keyboard Shortcuts",
        "Available Keyboard Shortcuts:\n\n"
        "Ctrl+G - Generate new password\n"
        "Ctrl+C - Copy password to clipboard\n"
        "F5 - Generate new password\n"
        "Alt+F4 - Exit application"
    )

def main():
    """Main function to run the password generator"""
    # Initialize GUI
    initialize_gui()
    configure_styles()
    
    # Create GUI components
    create_title()
    create_length_section()
    create_options_section()
    create_buttons_section()
    create_password_display()
    create_strength_indicator()
    
    # Setup additional features
    create_menu()
    setup_keyboard_shortcuts()
    
    # Generate initial password
    generate_password()
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    # Start the GUI main loop
    root.mainloop()

if __name__ == "__main__":
    main()
