# gui.py — version 1.3
# Author: Adam Pluguez
# Date: 2025-07-16
# License: This code is free to use and modify under the MIT License.

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit,
    QListWidget, QListWidgetItem, QLabel, QMessageBox, QDialog
)
from PyQt6.QtCore import Qt
from torrentbot import TorrentBot
from settingsdialog import SettingsDialog
import requests

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AutoTorrent")
        self.resize(600, 550)
        layout = QVBoxLayout(self)

        # Search input box
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search query")
        layout.addWidget(self.search_input)

        # Search button
        self.btn_search = QPushButton("Search")
        self.btn_search.clicked.connect(self.do_search)
        layout.addWidget(self.btn_search)

        # Results list section
        layout.addWidget(QLabel("Results:"))
        self.results_list = QListWidget()
        layout.addWidget(self.results_list)

        # Status label for count
        self.status_lbl = QLabel("Results found: 0")
        layout.addWidget(self.status_lbl)

        # Buttons for torrent actions and settings
        self.btn_add = QPushButton("Add Selected")
        self.btn_add.clicked.connect(self.on_add)

        self.btn_settings = QPushButton("Settings…")
        self.btn_settings.clicked.connect(self.open_settings)

        layout.addWidget(self.btn_add)
        layout.addWidget(self.btn_settings)

        # Load initial settings and bot
        self.load_settings()

    def load_settings(self):
        # Load settings via SettingsDialog and initialize TorrentBot
        dlg = SettingsDialog(self)
        dlg.load_settings()
        if dlg.exec() == QDialog.DialogCode.Accepted:
            pass  # User pressed OK in dialog
        self.settings = dlg.settings
        self.bot = TorrentBot(
            host=self.settings.value("host"),
            port=int(self.settings.value("port")),
            user=self.settings.value("user"),
            password=self.settings.value("password"),
            download_dir=self.settings.value("dir")
        )
        self.limit = int(self.settings.value("limit"))

    def open_settings(self):
        # Show the settings dialog again
        dlg = SettingsDialog(self)
        dlg.load_settings()
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.load_settings()

    def do_search(self):
        # Search button callback: runs the magnet search and populates results
        q = self.search_input.text().strip()
        if not q:
            QMessageBox.warning(self, "Warning", "Please enter a search query.")
            return
        try:
            found = self.bot.search_magnets(q, limit=self.limit)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Search failed: {e}")
            return

        # Populate results in the UI
        self.results_list.clear()
        for title, link in found:
            item = QListWidgetItem(title)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            item.setData(Qt.ItemDataRole.UserRole, (title, link))
            self.results_list.addItem(item)

        self.status_lbl.setText(f"Results found: {len(found)}")

    def on_add(self):
        # Add selected torrents to Transmission
        selections = []
        for i in range(self.results_list.count()):
            item = self.results_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                selections.append(item.data(Qt.ItemDataRole.UserRole))
        if not selections:
            QMessageBox.information(self, "No selection", "No torrents selected.")
            return

        try:
            added = self.bot.add_torrents(selections)
            QMessageBox.information(self, "Success", f"Added {added} torrent(s).")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

# Main entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
