"""Dialog helpers for user notifications."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox


class AppDialogs:
    """Show professional error and info dialogs."""

    @staticmethod
    def show_error(parent: tk.Misc, message: str) -> None:
        """Display an error dialog."""
        messagebox.showerror("CipherLab Error", message, parent=parent)

    @staticmethod
    def show_info(parent: tk.Misc, message: str) -> None:
        """Display an informational message."""
        messagebox.showinfo("CipherLab", message, parent=parent)
