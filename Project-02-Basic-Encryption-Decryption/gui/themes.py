"""Theme styling for the CipherLab interface."""

from __future__ import annotations

import customtkinter as ctk


class AppTheme:
    """Centralized dark-theme styling for the application."""

    @staticmethod
    def apply_theme(root: ctk.CTk) -> None:
        """Apply a modern dark theme to the Tkinter application."""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        root.title("CipherLab")
        root.configure(fg_color="#0f172a")
