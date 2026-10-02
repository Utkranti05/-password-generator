import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip


# ── Core Logic ──────────────────────────────────────────────────────────────

def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    """Generate a random password based on selected character sets."""
    charset = ""
    if use_upper:
        charset += string.ascii_uppercase
    if use_lower:
        charset += string.ascii_lowercase
    if use_digits:
        charset += string.digits
    if use_symbols:
        charset += string.punctuation

    if not charset:
        return None  # No character set selected

    # Ensure at least one character from each selected set
    guaranteed = []
    if use_upper:
        guaranteed.append(random.choice(string.ascii_uppercase))
    if use_lower:
        guaranteed.append(random.choice(string.ascii_lowercase))
    if use_digits:
        guaranteed.append(random.choice(string.digits))
    if use_symbols:
        guaranteed.append(random.choice(string.punctuation))

    remaining = [random.choice(charset) for _ in range(length - len(guaranteed))]
    password_list = guaranteed + remaining
    random.shuffle(password_list)
    return "".join(password_list)


def get_strength(length, use_upper, use_lower, use_digits, use_symbols):
    """Return a strength label based on length and character variety."""
    variety = sum([use_upper, use_lower, use_digits, use_symbols])
    if length >= 16 and variety >= 3:
        return "Strong 💪", "green"
    elif length >= 10 and variety >= 2:
        return "Medium ⚠️", "orange"
    else:
        return "Weak ❌", "red"


# ── GUI ─────────────────────────────────────────────────────────────────────

class PasswordGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Generator")
        self.resizable(False, False)
        self.configure(padx=20, pady=20, bg="#f0f0f0")

        self._build_ui()

    def _build_ui(self):
        bg = "#f0f0f0"
        font_label = ("Segoe UI", 10)
        font_title = ("Segoe UI", 14, "bold")

        # Title
        tk.Label(self, text="🔐 Password Generator", font=font_title,
                 bg=bg).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # Length slider
        tk.Label(self, text="Password Length:", font=font_label,
                 bg=bg).grid(row=1, column=0, sticky="w")
        self.length_var = tk.IntVar(value=12)
        self.length_label = tk.Label(self, text="12", font=font_label,
                                     bg=bg, width=3)
        self.length_label.grid(row=1, column=1, sticky="e")
        self.length_slider = tk.Scale(
            self, from_=4, to=64, orient="horizontal",
            variable=self.length_var, bg=bg, highlightthickness=0,
            command=self._update_length_label, length=260
        )
        self.length_slider.grid(row=2, column=0, columnspan=2, pady=(0, 10))

        # Checkboxes
        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=False)

        checks = [
            ("Uppercase  (A–Z)", self.use_upper),
            ("Lowercase  (a–z)", self.use_lower),
            ("Numbers    (0–9)", self.use_digits),
            ("Symbols (!@#$...)", self.use_symbols),
        ]
        for i, (label, var) in enumerate(checks):
            tk.Checkbutton(self, text=label, variable=var, font=font_label,
                           bg=bg, activebackground=bg).grid(
                row=3 + i, column=0, columnspan=2, sticky="w")

        # Number of passwords
        tk.Label(self, text="How many passwords:", font=font_label,
                 bg=bg).grid(row=7, column=0, sticky="w", pady=(10, 0))
        self.count_var = tk.IntVar(value=1)
        tk.Spinbox(self, from_=1, to=10, textvariable=self.count_var,
                   width=5, font=font_label).grid(row=7, column=1,
                                                   sticky="e", pady=(10, 0))

        # Generate button
        tk.Button(self, text="Generate Password", command=self._generate,
                  bg="#3b82d4", fg="white", font=("Segoe UI", 10, "bold"),
                  relief="flat", padx=10, pady=6, cursor="hand2").grid(
            row=8, column=0, columnspan=2, pady=(15, 8), sticky="ew")

        # Output box
        self.output_box = tk.Text(self, height=6, width=38,
                                  font=("Consolas", 11), relief="solid",
                                  bd=1, wrap="word", state="disabled")
        self.output_box.grid(row=9, column=0, columnspan=2, pady=(0, 8))

        # Strength label
        self.strength_label = tk.Label(self, text="", font=font_label, bg=bg)
        self.strength_label.grid(row=10, column=0, columnspan=2)

        # Copy button
        tk.Button(self, text="📋 Copy to Clipboard", command=self._copy,
                  bg="#6b7280", fg="white", font=("Segoe UI", 9),
                  relief="flat", padx=8, pady=4, cursor="hand2").grid(
            row=11, column=0, columnspan=2, pady=(8, 0), sticky="ew")

    def _update_length_label(self, val):
        self.length_label.config(text=str(int(float(val))))

    def _generate(self):
        length = self.length_var.get()
        upper = self.use_upper.get()
        lower = self.use_lower.get()
        digits = self.use_digits.get()
        symbols = self.use_symbols.get()
        count = self.count_var.get()

        if not any([upper, lower, digits, symbols]):
            messagebox.showwarning("No Options Selected",
                                   "Please select at least one character type.")
            return

        passwords = []
        for _ in range(count):
            pwd = generate_password(length, upper, lower, digits, symbols)
            if pwd:
                passwords.append(pwd)

        self.output_box.config(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.insert("end", "\n".join(passwords))
        self.output_box.config(state="disabled")

        label, color = get_strength(length, upper, lower, digits, symbols)
        self.strength_label.config(text=f"Strength: {label}", fg=color)

    def _copy(self):
        content = self.output_box.get("1.0", "end").strip()
        if not content:
            messagebox.showinfo("Nothing to Copy", "Generate a password first.")
            return
        # Copy only the first password if multiple were generated
        first_password = content.splitlines()[0]
        try:
            pyperclip.copy(first_password)
            messagebox.showinfo("Copied!", f"Password copied to clipboard:\n{first_password}")
        except Exception:
            # Fallback if pyperclip not installed
            self.clipboard_clear()
            self.clipboard_append(first_password)
            messagebox.showinfo("Copied!", f"Password copied to clipboard:\n{first_password}")


# ── Entry Point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()
