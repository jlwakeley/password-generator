import secrets
import string
import pyperclip
import tkinter as tk
from tkinter import ttk, messagebox


def generate_password(excluded_symbols: str, length: int) -> str:
    """
    Generate a password with the given length and excluded symbols
    """
    char_symb = string.ascii_letters + string.digits + string.punctuation
    for char in excluded_symbols:
        char_symb = char_symb.replace(char, "")
    if not char_symb:
        raise ValueError(
            "All symbols, numbers, and letters are excluded. Please try again."
        )
    return "".join(secrets.choice(char_symb) for i in range(length))


def generate_password_click(
    excluded_symbols_entry, length_entry, password_display
) -> None:
    excluded_symbols = excluded_symbols_entry.get()
    length = length_entry.get()
    try:
        length = int(length)
        if length <= 0:
            raise ValueError()
    except ValueError:
        messagebox.showerror(
            "Error", "Invalid length requirement. Please input a positive integer."
        )
        return

    try:
        password = generate_password(excluded_symbols, length)
    except ValueError:
        messagebox.showerror(
            "Error", "All symbols, numbers, and letters are excluded. Please try again."
        )
        return

    password_display.config(state=tk.NORMAL)
    password_display.delete("1.0", tk.END)
    password_display.insert(tk.END, password)
    password_display.config(state=tk.DISABLED)

    pyperclip.copy(password)


def copy_to_clipboard(password_display) -> None:
    password = password_display.get("1.0", tk.END).strip()
    pyperclip.copy(password)


def create_gui() -> None:
    window = tk.Tk()
    window.title("Password Generator")

    window_style = ttk.Style()
    window_style.theme_use("clam")

    main_frame = ttk.Frame(window, padding="20")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    font = ("Helvetica", 12)

    excluded_symbols_label = ttk.Label(
        main_frame, text="Exclude what symbols?", font=font
    )
    excluded_symbols_entry = ttk.Entry(main_frame, font=font)
    length_label = ttk.Label(main_frame, text="Length requirement?", font=font)
    length_entry = ttk.Entry(main_frame, font=font)
    generate_button = ttk.Button(
        main_frame,
        text="Generate Password",
        command=lambda: generate_password_click(
            excluded_symbols_entry, length_entry, password_display
        ),
        style="TButton",
    )
    copy_button = ttk.Button(
        main_frame,
        text="Copy to Clipboard",
        command=lambda: copy_to_clipboard(password_display),
        style="TButton",
    )
    password_display_label = ttk.Label(
        main_frame, text="Generated Password:", font=font
    )
    password_display = tk.Text(main_frame, height=1, width=30, font=font)
    password_display.config(state=tk.DISABLED)

    excluded_symbols_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    excluded_symbols_entry.grid(row=0, column=1, padx=5, pady=5)
    length_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
    length_entry.grid(row=1, column=1, padx=5, pady=5)
    generate_button.grid(
        row=2, column=0, columnspan=2, padx=5, pady=10, sticky=(tk.W, tk.E)
    )
    password_display_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
    password_display.grid(row=3, column=1, padx=5, pady=5)
    copy_button.grid(
        row=4, column=0, columnspan=2, padx=5, pady=10, sticky=(tk.W, tk.E)
    )

    window.mainloop()


def main() -> None:
    create_gui()


if __name__ == "__main__":
    main()
