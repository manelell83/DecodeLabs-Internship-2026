from __future__ import annotations

import json
import tkinter as tk
from typing import Any

import customtkinter as ctk

from core.password_analyzer import PasswordAnalyzer
from gui.themes import AppTheme


class MainWindow:
    """Main desktop window for the password strength analyzer."""

    def __init__(self) -> None:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.root = ctk.CTk()
        self.root.title("Password Strength Analyzer")
        self.root.geometry("980x720")
        self.root.minsize(900, 680)
        self.root.configure(fg_color=AppTheme.BACKGROUND)

        self.analyzer = PasswordAnalyzer()
        self.checklist_labels: dict[str, ctk.CTkLabel] = {}
        self._build_ui()

    def run(self) -> None:
        self.root.mainloop()

    def _build_ui(self) -> None:
        self._build_header()
        self._build_input_section()
        self._build_results_panel()
        self._build_actions_panel()

    def _build_header(self) -> None:
        header = ctk.CTkFrame(self.root, fg_color=AppTheme.BACKGROUND)
        header.pack(fill="x", padx=20, pady=(20, 12))

        title = ctk.CTkLabel(
            header,
            text="Password Strength Analyzer",
            font=("Segoe UI", 24, "bold"),
            text_color=AppTheme.TEXT,
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header,
            text="Professional password evaluation, entropy assessment, and risk insights.",
            font=("Segoe UI", 11),
            text_color=AppTheme.MUTED,
        )
        subtitle.pack(anchor="w", pady=(4, 0))

    def _build_input_section(self) -> None:
        card = ctk.CTkFrame(self.root, corner_radius=16, fg_color=AppTheme.PANEL)
        card.pack(fill="x", padx=20, pady=(0, 12))

        ctk.CTkLabel(card, text="Password", font=("Segoe UI", 12, "bold"), text_color=AppTheme.TEXT).pack(anchor="w", padx=16, pady=(14, 0))

        self.password_var = tk.StringVar()
        entry_frame = ctk.CTkFrame(card, fg_color=AppTheme.PANEL_ALT)
        entry_frame.pack(fill="x", padx=16, pady=14)

        self.password_entry = ctk.CTkEntry(
            entry_frame,
            textvariable=self.password_var,
            show="●",
            font=("Segoe UI", 13),
            width=560,
            border_color=AppTheme.ACCENT,
            fg_color=AppTheme.PANEL_ALT,
            text_color=AppTheme.TEXT,
        )
        self.password_entry.pack(side="left", fill="x", expand=True, padx=8, pady=8)
        self.password_entry.bind("<KeyRelease>", self._on_password_change)

        self.toggle_button = ctk.CTkButton(entry_frame, text="Show", command=self._toggle_visibility, width=70)
        self.toggle_button.pack(side="left", padx=(0, 8), pady=8)

    def _build_results_panel(self) -> None:
        main = ctk.CTkFrame(self.root, fg_color=AppTheme.BACKGROUND)
        main.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        left = ctk.CTkFrame(main, fg_color=AppTheme.BACKGROUND)
        left.pack(side="left", fill="both", expand=True)

        self.score_frame = ctk.CTkFrame(left, corner_radius=16, fg_color=AppTheme.PANEL)
        self.score_frame.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(self.score_frame, text="Strength Score", font=("Segoe UI", 12, "bold"), text_color=AppTheme.TEXT).pack(anchor="w", padx=16, pady=(14, 0))

        self.score_var = tk.StringVar(value="0 / 100")
        ctk.CTkLabel(self.score_frame, textvariable=self.score_var, font=("Segoe UI", 28, "bold"), text_color=AppTheme.ACCENT).pack(anchor="w", padx=16, pady=(8, 6))

        self.progress = ctk.CTkProgressBar(self.score_frame, width=420)
        self.progress.pack(fill="x", padx=16, pady=(6, 0))
        self.progress.set(0)

        self.level_var = tk.StringVar(value="Weak")
        ctk.CTkLabel(self.score_frame, textvariable=self.level_var, font=("Segoe UI", 11, "bold"), text_color=AppTheme.WARNING).pack(anchor="w", padx=16, pady=(8, 16))

        info_frame = ctk.CTkFrame(left, corner_radius=16, fg_color=AppTheme.PANEL)
        info_frame.pack(fill="x")

        ctk.CTkLabel(info_frame, text="Security Metrics", font=("Segoe UI", 12, "bold"), text_color=AppTheme.TEXT).pack(anchor="w", padx=16, pady=(14, 0))
        self.entropy_var = tk.StringVar(value="Entropy: 0 bits")
        self.bruteforce_var = tk.StringVar(value="Brute-force estimate: N/A")
        self.guess_var = tk.StringVar(value="Estimated guesses: 0")

        for variable in (self.entropy_var, self.bruteforce_var, self.guess_var):
            ctk.CTkLabel(info_frame, textvariable=variable, font=("Segoe UI", 11), text_color=AppTheme.MUTED).pack(anchor="w", padx=16, pady=(6, 0))

        right = ctk.CTkFrame(main, fg_color=AppTheme.BACKGROUND)
        right.pack(side="left", fill="both", expand=True, padx=(12, 0))

        checklist_frame = ctk.CTkFrame(right, corner_radius=16, fg_color=AppTheme.PANEL)
        checklist_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(checklist_frame, text="Checklist", font=("Segoe UI", 12, "bold"), text_color=AppTheme.TEXT).pack(anchor="w", padx=16, pady=(14, 0))
        for item in [
            "minimum_length",
            "uppercase",
            "lowercase",
            "number",
            "special",
            "pattern_free",
            "common_password",
        ]:
            label = ctk.CTkLabel(checklist_frame, text="●", font=("Segoe UI", 11), text_color=AppTheme.MUTED)
            label.pack(anchor="w", padx=16, pady=(5, 0))
            self.checklist_labels[item] = label

        suggestions_frame = ctk.CTkFrame(right, corner_radius=16, fg_color=AppTheme.PANEL)
        suggestions_frame.pack(fill="x", pady=(12, 0))

        ctk.CTkLabel(suggestions_frame, text="Suggestions", font=("Segoe UI", 12, "bold"), text_color=AppTheme.TEXT).pack(anchor="w", padx=16, pady=(14, 0))
        self.suggestions_text = tk.Text(suggestions_frame, height=8, wrap="word", bg=AppTheme.PANEL_ALT, fg=AppTheme.TEXT, insertbackground="#ffffff")
        self.suggestions_text.pack(fill="x", padx=16, pady=(0, 14))

    def _build_actions_panel(self) -> None:
        actions = ctk.CTkFrame(self.root, fg_color=AppTheme.BACKGROUND)
        actions.pack(fill="x", padx=20, pady=(0, 20))

        self.copy_button = ctk.CTkButton(actions, text="Copy Password", command=self._copy_password)
        self.copy_button.pack(side="left")

        self.generate_button = ctk.CTkButton(actions, text="Generate Secure Password", command=self._generate_password)
        self.generate_button.pack(side="left", padx=(8, 0))

        self.export_button = ctk.CTkButton(actions, text="Export JSON", command=self._export_json)
        self.export_button.pack(side="left", padx=(8, 0))

    def _on_password_change(self, _event: Any) -> None:
        password = self.password_var.get()
        result = self.analyzer.analyze(password)
        self._render_result(result)

    def _render_result(self, result: Any) -> None:
        self.score_var.set(f"{result.score} / 100")
        self.level_var.set(result.level)
        self.progress.set(result.score / 100)
        self.entropy_var.set(f"Entropy: {result.entropy:.1f} bits")
        self.bruteforce_var.set(f"Brute-force estimate: {result.brute_force_time}")
        self.guess_var.set(f"Estimated guesses: {result.estimated_guesses:,}")

        for key, value in result.checklist.items():
            label = self.checklist_labels.get(key)
            if label is None:
                continue
            state = "✓" if value else "✗"
            color = AppTheme.ACCENT if value else AppTheme.DANGER
            label.configure(text=f"{state} {self._friendly_label(key)}", text_color=color)

        self.suggestions_text.delete("1.0", tk.END)
        self.suggestions_text.insert(tk.END, "\n".join(result.suggestions))

    def _friendly_label(self, key: str) -> str:
        labels = {
            "minimum_length": "Minimum length (12+ characters)",
            "uppercase": "Contains uppercase letters",
            "lowercase": "Contains lowercase letters",
            "number": "Contains numbers",
            "special": "Contains special symbols",
            "pattern_free": "No repeated patterns",
            "common_password": "Common password detected",
        }
        return labels.get(key, key.replace("_", " ").title())

    def _toggle_visibility(self) -> None:
        current = self.password_entry.cget("show")
        self.password_entry.configure(show="" if current == "●" else "●")
        self.toggle_button.configure(text="Hide" if current == "●" else "Show")

    def _copy_password(self) -> None:
        self.root.clipboard_clear()
        self.root.clipboard_append(self.password_var.get())
        self.root.update()

    def _generate_password(self) -> None:
        password = PasswordAnalyzer.generate_secure_password(16)
        self.password_var.set(password)
        self._on_password_change(None)

    def _export_json(self) -> None:
        data = self.analyzer.analyze(self.password_var.get())
        payload = {
            "password": data.password,
            "score": data.score,
            "entropy": round(data.entropy, 2),
            "level": data.level,
            "checklist": data.checklist,
            "suggestions": data.suggestions,
            "flags": data.flags,
            "brute_force_time": data.brute_force_time,
            "estimated_guesses": data.estimated_guesses,
        }
        export_path = "analysis_export.json"
        with open(export_path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)


if __name__ == "__main__":
    MainWindow().run()
