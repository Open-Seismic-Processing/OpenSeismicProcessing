"""
Utility helpers for managing survey workspaces.

Currently provides a single function `select_workspace_folder` that prompts the
user for a root directory using a native folder-selection dialog. The selected
path is returned as a string (or `None` if the user cancels).
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

try:
    # Tkinter ships with Python and gives us a simple native folder dialog.
    from tkinter import Tk, filedialog
except ImportError as exc:  # pragma: no cover - should not happen in std envs
    raise RuntimeError("Tkinter is required for folder selection dialogs") from exc


def select_workspace_folder(initial_dir: Optional[str] = None) -> Optional[str]:
    """
    Open a folder-selection dialog and return the chosen path.

    Parameters
    ----------
    initial_dir:
        Optional starting directory for the dialog. Falls back to the user's
        home directory if the provided path is invalid or missing.

    Returns
    -------
    Optional[str]
        Absolute path to the selected folder, or None if the dialog was
        cancelled.
    """
    root = Tk()
    root.withdraw()  # Hide the empty Tk window
    root.update()

    start_dir = Path(initial_dir).expanduser().resolve() if initial_dir else Path.home()
    if not start_dir.exists():
        start_dir = Path.home()

    selected_path = filedialog.askdirectory(
        parent=root,
        initialdir=str(start_dir),
        title="Select workspace root folder",
        mustexist=True,
    )

    root.destroy()

    if not selected_path:
        return None

    return os.path.abspath(selected_path)
