from PyQt6 import QtWidgets


def show_3d_viewer(window):
    """Placeholder 3D viewer tab."""
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(widget)
    layout.addWidget(QtWidgets.QLabel("3D Viewer (not implemented yet)"))
    window.tabWidget.addTab(widget, "3D Viewer")
    window.tabWidget.setCurrentWidget(widget)
