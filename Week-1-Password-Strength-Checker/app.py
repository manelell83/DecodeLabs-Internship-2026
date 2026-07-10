from __future__ import annotations

import sys
from pathlib import Path

from gui.main_window import MainWindow


def main() -> None:
    """Launch the password strength analyzer application."""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
