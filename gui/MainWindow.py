from SurveyDialogs import NewSurveyDialog, DialogBox, ImportSEGYDialog
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QIcon, QAction
import sys
import os
import numpy as np
from openseismicprocessing.catalog import init_db, get_workspace_root, set_workspace_root, list_projects

class OpenSeismicProcessingWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("golem.ui", self)  # Load main window UI
        
        init_db()
        stored_root = get_workspace_root()
        # Initialize variables
        self.rootFolderPath = stored_root if stored_root and os.path.isdir(stored_root) else ""
        self.currentSurveyPath = None
        self.currentSurveyName = None
        
        # Find the QAction by its objectName in Qt Designer
        self.actionSetRootFolder = self.findChild(QAction, "action_Set_Root_Folder")
        self.actionSetupSurvey = self.findChild(QAction, "action_Select_Setup")  # Add your QAction here
        self.actionLoadSegy = self.findChild(QAction, "action_Seg_y_file")

        # Connect QAction to their respective functions
        self.actionSetRootFolder.triggered.connect(self.SelectRootFolder)
        self.actionSetupSurvey.triggered.connect(self.SetupSurvey)  # Call the dialog
        if self.actionLoadSegy:
            self.actionLoadSegy.triggered.connect(self.LoadSegyFiles)

        # ✅ Set up an initial empty visualization
        # self.init_empty_visualization()    

    def SelectRootFolder(self):
        """Opens a dialog to select a folder."""
        selected = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder")
        if selected:
            self.rootFolderPath = selected
            set_workspace_root(selected)

    def SetupSurvey(self):
        """Opens the custom dialog."""
        
        if not self.rootFolderPath:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please select a root folder first!")
            return
        # Get the list of folder names from the root directory
        self.folder_list = [
           folder for folder in os.listdir(self.rootFolderPath)
           if os.path.isdir(os.path.join(self.rootFolderPath, folder))
       ]

        dialog = DialogBox(self, selected_survey=self.currentSurveyName)  # Instantiate the custom dialog
        if dialog.exec():  # Show the dialog and wait for it to close
            selected = dialog.GetSelectedSurvey()
            if selected:
                self.currentSurveyName = selected
                self.currentSurveyPath = os.path.join(self.rootFolderPath, selected)
           
        else:
            print("Dialog Closed!")
    
    def LoadSegyFiles(self):
        if not self.rootFolderPath:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please select a root folder first!")
            return
        boundary = None
        if self.currentSurveyName:
            try:
                project = next(p for p in list_projects() if p["name"] == self.currentSurveyName)
                metadata = project.get("metadata", {}) or {}
                boundary = metadata.get("boundary", metadata)
            except StopIteration:
                boundary = None
        dialog = ImportSEGYDialog(boundary=boundary)
        dialog.exec()
