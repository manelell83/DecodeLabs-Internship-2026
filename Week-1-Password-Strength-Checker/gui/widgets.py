from __future__ import annotations

import customtkinter as ctk


class StatusBadge(ctk.CTkFrame):
    """Small reusable badge for showing boolean state in the UI."""

    def __init__(self, master: ctk.CTkFrame, text: str, *, positive: bool = True) -> None:
        super().__init__(master, fg_color="transparent")
        self.label = ctk.CTkLabel(
            self,
            text=text,
            font=("Segoe UI", 11),
            text_color="#6ee7b7" if positive else "#ff6b6b",
        )
        self.label.pack(anchor="w")
