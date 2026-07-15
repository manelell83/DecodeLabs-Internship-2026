"""Main application window for CipherLab."""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import customtkinter as ctk

from core.caesar_cipher import CaesarCipher
from core.file_handler import FileHandler
from core.history_manager import HistoryManager
from core.validators import ValidationError, validate_keyword, validate_shift, validate_text
from core.vigenere_cipher import VigenereCipher
from gui.dialogs import AppDialogs
from gui.themes import AppTheme
from gui.widgets import ActionButton, SectionLabel
from utils.constants import APP_TITLE, APP_VERSION, WINDOW_HEIGHT, WINDOW_WIDTH
from utils.helpers import truncate


class CipherLabApp(ctk.CTk):
    """Main window for the CipherLab desktop app."""

    def __init__(self) -> None:
        super().__init__()
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Create the layout and bind shortcuts."""
        AppTheme.apply_theme(self)
        self._build_menu()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, corner_radius=18)
        header.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))
        header.grid_columnconfigure(1, weight=1)

        title = ctk.CTkLabel(
            header,
            text=f"{APP_TITLE} v{APP_VERSION}",
            font=("Segoe UI", 24, "bold"),
        )
        title.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Modern classical cipher toolkit for learning and experimentation",
            font=("Segoe UI", 12),
        )
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        self.main_frame = ctk.CTkFrame(self, corner_radius=20)
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.left_panel = ctk.CTkFrame(self.main_frame, width=320, corner_radius=18)
        self.left_panel.grid(row=0, column=0, sticky="ns", padx=(15, 10), pady=15)
        self.left_panel.grid_columnconfigure(0, weight=1)

        self.right_panel = ctk.CTkFrame(self.main_frame, corner_radius=18)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 15), pady=15)
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=1)

        self._build_left_panel()
        self._build_right_panel()
        self._bind_shortcuts()

        self.caesar_cipher = CaesarCipher()
        self.vigenere_cipher = VigenereCipher()
        self.file_handler = FileHandler()
        self.history_manager = HistoryManager()

        self.status_var = ctk.StringVar(value="Ready")
        self.status_bar = ctk.CTkLabel(self, textvariable=self.status_var, anchor="w")
        self.status_bar.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))

    def _build_menu(self) -> None:
        """Create the top-level menu bar."""
        menu = tk.Menu(self)
        self.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Import TXT", accelerator="Ctrl+O", command=self.import_text)
        file_menu.add_command(label="Export", accelerator="Ctrl+S", command=self.export_output)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)
        menu.add_cascade(label="File", menu=file_menu)

        cipher_menu = tk.Menu(menu, tearoff=0)
        cipher_menu.add_command(label="Caesar", command=lambda: self.set_cipher_mode("caesar"))
        cipher_menu.add_command(label="Vigenère", command=lambda: self.set_cipher_mode("vigenere"))
        menu.add_cascade(label="Cipher", menu=cipher_menu)

        history_menu = tk.Menu(menu, tearoff=0)
        history_menu.add_command(label="View History", command=self.show_history)
        history_menu.add_command(label="Clear History", command=self.clear_history)
        menu.add_cascade(label="History", menu=history_menu)

        help_menu = tk.Menu(menu, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu.add_cascade(label="Help", menu=help_menu)

    def _build_left_panel(self) -> None:
        """Create the configuration sidebar."""
        SectionLabel(self.left_panel, "Cipher Mode").grid(row=0, column=0, padx=15, pady=(15, 8), sticky="w")

        self.mode_var = ctk.StringVar(value="caesar")
        self.mode_switch = ctk.CTkSegmentedButton(
            self.left_panel,
            values=["Caesar", "Vigenère"],
            command=self.set_cipher_mode,
            variable=self.mode_var,
        )
        self.mode_switch.grid(row=1, column=0, padx=15, pady=(0, 12), sticky="ew")

        SectionLabel(self.left_panel, "Controls").grid(row=2, column=0, padx=15, pady=(8, 8), sticky="w")
        self.encrypt_button = ActionButton(self.left_panel, "Encrypt", command=self.encrypt_text)
        self.encrypt_button.grid(row=3, column=0, padx=15, pady=6, sticky="ew")

        self.decrypt_button = ActionButton(self.left_panel, "Decrypt", command=self.decrypt_text)
        self.decrypt_button.grid(row=4, column=0, padx=15, pady=6, sticky="ew")

        self.clear_button = ActionButton(self.left_panel, "Clear", command=self.clear_fields)
        self.clear_button.grid(row=5, column=0, padx=15, pady=6, sticky="ew")

        self.copy_button = ActionButton(self.left_panel, "Copy Output", command=self.copy_output)
        self.copy_button.grid(row=6, column=0, padx=15, pady=6, sticky="ew")

        self.import_button = ActionButton(self.left_panel, "Import TXT", command=self.import_text)
        self.import_button.grid(row=7, column=0, padx=15, pady=6, sticky="ew")

        self.export_button = ActionButton(self.left_panel, "Export TXT", command=self.export_output)
        self.export_button.grid(row=8, column=0, padx=15, pady=6, sticky="ew")

        self.history_button = ActionButton(self.left_panel, "History", command=self.show_history)
        self.history_button.grid(row=9, column=0, padx=15, pady=(6, 15), sticky="ew")

    def _build_right_panel(self) -> None:
        """Create the main text entry and output panel."""
        SectionLabel(self.right_panel, "Plain Text").grid(row=0, column=0, padx=15, pady=(15, 8), sticky="w")
        self.input_text = ctk.CTkTextbox(self.right_panel, height=140, corner_radius=12)
        self.input_text.grid(row=1, column=0, padx=15, pady=(0, 12), sticky="nsew")

        self.shift_label = ctk.CTkLabel(self.right_panel, text="Shift Key")
        self.shift_label.grid(row=2, column=0, padx=15, pady=(0, 6), sticky="w")
        self.shift_entry = ctk.CTkEntry(self.right_panel)
        self.shift_entry.grid(row=3, column=0, padx=15, pady=(0, 12), sticky="ew")

        self.keyword_label = ctk.CTkLabel(self.right_panel, text="Keyword")
        self.keyword_label.grid(row=4, column=0, padx=15, pady=(0, 6), sticky="w")
        self.keyword_entry = ctk.CTkEntry(self.right_panel)
        self.keyword_entry.grid(row=5, column=0, padx=15, pady=(0, 12), sticky="ew")

        SectionLabel(self.right_panel, "Output").grid(row=6, column=0, padx=15, pady=(4, 8), sticky="w")
        self.output_text = ctk.CTkTextbox(self.right_panel, height=140, corner_radius=12)
        self.output_text.grid(row=7, column=0, padx=15, pady=(0, 12), sticky="nsew")

        self.right_panel.grid_rowconfigure(1, weight=1)
        self.right_panel.grid_rowconfigure(7, weight=1)

    def _bind_shortcuts(self) -> None:
        """Bind keyboard shortcuts for common actions."""
        self.bind_all("<Control-o>", lambda event: self.import_text())
        self.bind_all("<Control-s>", lambda event: self.export_output())
        self.bind_all("<Control-l>", lambda event: self.clear_fields())
        self.bind_all("<Control-c>", lambda event: self.copy_output())

    def set_cipher_mode(self, mode: str) -> None:
        """Switch between Caesar and Vigenère modes."""
        self.mode_var.set("caesar" if mode == "caesar" else "vigenere")
        self.status_var.set(f"Mode switched to {mode.title()}")
        if mode == "caesar":
            self.keyword_entry.configure(state="disabled")
            self.shift_label.configure(text="Shift Key")
        else:
            self.keyword_entry.configure(state="normal")
            self.shift_label.configure(text="Shift Key (ignored for Vigenère)")

    def encrypt_text(self) -> None:
        """Encrypt the current input using the selected cipher."""
        try:
            text = validate_text(self.input_text.get("1.0", "end"))
            if self.mode_var.get() == "caesar":
                shift = validate_shift(self.shift_entry.get())
                result = self.caesar_cipher.encrypt(text, shift)
                self.output_text.delete("1.0", "end")
                self.output_text.insert("1.0", result)
                self.history_manager.add_entry(
                    cipher="Caesar",
                    operation="Encrypt",
                    key=str(shift),
                    input_preview=truncate(text),
                    output_preview=truncate(result),
                )
            else:
                keyword = validate_keyword(self.keyword_entry.get())
                result = self.vigenere_cipher.encrypt(text, keyword)
                self.output_text.delete("1.0", "end")
                self.output_text.insert("1.0", result)
                self.history_manager.add_entry(
                    cipher="Vigenère",
                    operation="Encrypt",
                    key=keyword,
                    input_preview=truncate(text),
                    output_preview=truncate(result),
                )
            self.status_var.set("Encryption complete")
        except ValidationError as exc:
            AppDialogs.show_error(self, str(exc))
        except Exception as exc:  # pragma: no cover - UI error handling
            AppDialogs.show_error(self, f"Unexpected error: {exc}")

    def decrypt_text(self) -> None:
        """Decrypt the current input using the selected cipher."""
        try:
            text = validate_text(self.input_text.get("1.0", "end"))
            if self.mode_var.get() == "caesar":
                shift = validate_shift(self.shift_entry.get())
                result = self.caesar_cipher.decrypt(text, shift)
                self.output_text.delete("1.0", "end")
                self.output_text.insert("1.0", result)
                self.history_manager.add_entry(
                    cipher="Caesar",
                    operation="Decrypt",
                    key=str(shift),
                    input_preview=truncate(text),
                    output_preview=truncate(result),
                )
            else:
                keyword = validate_keyword(self.keyword_entry.get())
                result = self.vigenere_cipher.decrypt(text, keyword)
                self.output_text.delete("1.0", "end")
                self.output_text.insert("1.0", result)
                self.history_manager.add_entry(
                    cipher="Vigenère",
                    operation="Decrypt",
                    key=keyword,
                    input_preview=truncate(text),
                    output_preview=truncate(result),
                )
            self.status_var.set("Decryption complete")
        except ValidationError as exc:
            AppDialogs.show_error(self, str(exc))
        except Exception as exc:  # pragma: no cover - UI error handling
            AppDialogs.show_error(self, f"Unexpected error: {exc}")

    def copy_output(self) -> None:
        """Copy the current output to the clipboard."""
        self.clipboard_clear()
        self.clipboard_append(self.output_text.get("1.0", "end"))
        self.update()
        self.status_var.set("Output copied")

    def clear_fields(self) -> None:
        """Clear all input and output fields."""
        self.input_text.delete("1.0", "end")
        self.output_text.delete("1.0", "end")
        self.shift_entry.delete(0, "end")
        self.keyword_entry.delete(0, "end")
        self.status_var.set("Cleared")

    def import_text(self) -> None:
        """Import text from a .txt file."""
        try:
            path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
            if not path:
                return
            content = self.file_handler.read_text(path)
            self.input_text.delete("1.0", "end")
            self.input_text.insert("1.0", content)
            self.status_var.set(f"Imported {path}")
        except Exception as exc:  # pragma: no cover - UI error handling
            AppDialogs.show_error(self, str(exc))

    def export_output(self) -> None:
        """Export the current output to a .txt file."""
        try:
            path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if not path:
                return
            self.file_handler.write_text(path, self.output_text.get("1.0", "end"))
            self.status_var.set(f"Exported {path}")
        except Exception as exc:  # pragma: no cover - UI error handling
            AppDialogs.show_error(self, str(exc))

    def show_history(self) -> None:
        """Show the operation history in a message box."""
        history = self.history_manager.read_history()
        if not history:
            AppDialogs.show_info(self, "No history recorded yet.")
            return

        lines = []
        for item in history:
            lines.append(
                f"{item['date']} {item['time']} | {item['cipher']} | {item['operation']} | {item['key']} | {item['input_preview']} -> {item['output_preview']}"
            )
        messagebox.showinfo("CipherLab History", "\n".join(lines[-10:]), parent=self)

    def clear_history(self) -> None:
        """Clear the saved operation history."""
        self.history_manager.clear_history()
        AppDialogs.show_info(self, "History cleared.")

    def show_about(self) -> None:
        """Show an About dialog."""
        messagebox.showinfo(
            "About CipherLab",
            f"CipherLab v{APP_VERSION}\nA modern classical cipher learning tool.",
            parent=self,
        )


def main() -> None:
    """Create and run the application."""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = CipherLabApp()
    app.mainloop()
