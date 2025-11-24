#!/usr/bin/env python3
"""Launcher for the Open Seismic Processing GUI."""

from PyQt6.QtWidgets import QApplication
import sys

from MainWindow import OpenSeismicProcessingWindow


def main() -> int:
    app = QApplication(sys.argv)
    window = OpenSeismicProcessingWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
