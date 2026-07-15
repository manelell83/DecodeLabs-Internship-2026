"""Reusable widgets for the CipherLab GUI."""

from __future__ import annotations

import customtkinter as ctk


class SectionLabel(ctk.CTkLabel):
    """A styled section title label."""

    def __init__(self, master: ctk.CTkBaseClass, text: str) -> None:
        super().__init__(master, text=text, font=("Segoe UI", 16, "bold"))


class ActionButton(ctk.CTkButton):
    """A reusable action button with consistent padding."""

    def __init__(self, master: ctk.CTkBaseClass, text: str, command=None) -> None:
        super().__init__(master, text=text, command=command, height=34)
