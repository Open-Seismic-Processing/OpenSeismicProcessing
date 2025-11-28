from PyQt6 import QtWidgets
from openseismicprocessing.catalog import set_workspace_root


def select_root_folder(window):
    """Let the user pick a root folder and store it on the window instance."""
    dlg = QtWidgets.QFileDialog(window, "Select Folder")
    dlg.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)
    dlg.setOptions(
        QtWidgets.QFileDialog.Option.DontUseNativeDialog
        | QtWidgets.QFileDialog.Option.ShowDirsOnly
    )
    if dlg.exec():
        selected = dlg.selectedFiles()
        if selected:
            window.rootFolderPath = selected[0]
            set_workspace_root(selected[0])
