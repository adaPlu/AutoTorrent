# torrentbot.py — version 1.3
# Author: Adam Pluguez
# Date: 2025-07-16
# License: This code is free to use and modify under the MIT License.
import os
from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QSpinBox,
    QDialogButtonBox, QMessageBox
)
from PyQt6.QtCore import QSettings

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.settings = QSettings("TorrentBot", "TorrentBotApp")
        layout = QFormLayout(self)

        self.ed_host = QLineEdit()
        self.ed_port = QLineEdit()
        self.ed_user = QLineEdit()
        self.ed_pass = QLineEdit()
        self.ed_dir = QLineEdit()
        self.spin_limit = QSpinBox()
        self.spin_limit.setRange(1, 50)

        layout.addRow("Host:", self.ed_host)
        layout.addRow("Port:", self.ed_port)
        layout.addRow("Username:", self.ed_user)
        layout.addRow("Password:", self.ed_pass)
        layout.addRow("Download dir:", self.ed_dir)
        layout.addRow("Results limit:", self.spin_limit)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addRow(self.buttons)

    def load_settings(self):
        # Set defaults if first launch
        if not self.settings.contains("host"):
            self.settings.setValue("host", "//192.168.0.170/")
            self.settings.setValue("port", 9091)
            self.settings.setValue("user", "transmission")
            self.settings.setValue("password", "transmission")
            self.settings.setValue("dir", "//192.168.0.17/tv/feed/")
            self.settings.setValue("limit", 25)

        self.ed_host.setText(self.settings.value("host"))
        self.ed_port.setText(str(self.settings.value("port")))
        self.ed_user.setText(self.settings.value("user"))
        self.ed_pass.setText(self.settings.value("password"))
        self.ed_dir.setText(self.settings.value("dir"))
        self.spin_limit.setValue(int(self.settings.value("limit")))

    def accept(self):
        # Validate essential fields
        if not self.ed_host.text().strip():
            QMessageBox.warning(self, "Warning", "Host cannot be empty.")
            return
        # Save settings
        self.settings.setValue("host", self.ed_host.text().strip())
        self.settings.setValue("port", int(self.ed_port.text().strip()))
        self.settings.setValue("user", self.ed_user.text().strip())
        self.settings.setValue("password", self.ed_pass.text().strip())
        self.settings.setValue("dir", self.ed_dir.text().strip())
        self.settings.setValue("limit", self.spin_limit.value())
        super().accept()
