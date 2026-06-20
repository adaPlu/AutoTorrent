# gui.py — version 1.4
# Author: Adam Pluguez
# Date: 2025-07-16
# License: This code is free to use and modify under the MIT License.

import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QMessageBox,
    QDialog
)

from PyQt6.QtCore import Qt

from torrentbot import TorrentBot
from settingsdialog import SettingsDialog


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AutoTorrent")
        self.resize(600, 550)

        layout = QVBoxLayout(self)

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Enter search query"
        )
        self.search_input.returnPressed.connect(
            self.do_search
        )
        layout.addWidget(self.search_input)

        # Search button
        self.btn_search = QPushButton("Search")
        self.btn_search.clicked.connect(
            self.do_search
        )
        layout.addWidget(self.btn_search)

        # Results
        layout.addWidget(QLabel("Results:"))

        self.results_list = QListWidget()
        layout.addWidget(self.results_list)

        # Status label
        self.status_lbl = QLabel(
            "Results found: 0"
        )
        layout.addWidget(self.status_lbl)

        # Buttons
        self.btn_add = QPushButton(
            "Add Selected"
        )
        self.btn_add.clicked.connect(
            self.on_add
        )

        self.btn_settings = QPushButton(
            "Settings..."
        )
        self.btn_settings.clicked.connect(
            self.open_settings
        )

        layout.addWidget(self.btn_add)
        layout.addWidget(self.btn_settings)

        self.load_settings()

    def load_settings(self):

        dlg = SettingsDialog(self)
        dlg.load_settings()

        if dlg.exec() == QDialog.DialogCode.Accepted:
            pass

        self.settings = dlg.settings

        self.bot = TorrentBot(
            host=self.settings.value("host"),
            port=int(self.settings.value("port")),
            user=self.settings.value("user"),
            password=self.settings.value("password"),
            download_dir=self.settings.value("dir")
        )

        self.limit = int(
            self.settings.value("limit")
        )

    def open_settings(self):

        dlg = SettingsDialog(self)
        dlg.load_settings()

        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.load_settings()

    def do_search(self):

        q = self.search_input.text().strip()

        if not q:
            QMessageBox.warning(
                self,
                "Warning",
                "Please enter a search query."
            )
            return

        try:
            found = self.bot.search_magnets_with_pagination(
                q,
                limit=self.limit
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                f"Search failed: {e}"
            )
            return

        self.results_list.clear()

        for title, link, seeders in found:

            display_text = (
                f"[{seeders}] {title}"
            )

            item = QListWidgetItem(
                display_text
            )

            item.setFlags(
                item.flags()
                | Qt.ItemFlag.ItemIsUserCheckable
            )

            item.setCheckState(
                Qt.CheckState.Unchecked
            )

            item.setData(
                Qt.ItemDataRole.UserRole,
                (
                    title,
                    link,
                    seeders
                )
            )

            self.results_list.addItem(item)

        self.status_lbl.setText(
            f"Results found: {len(found)}"
        )

    def on_add(self):

        selections = []

        for i in range(
            self.results_list.count()
        ):

            item = self.results_list.item(i)

            if (
                item.checkState()
                == Qt.CheckState.Checked
            ):
                selections.append(
                    item.data(
                        Qt.ItemDataRole.UserRole
                    )
                )

        if not selections:

            QMessageBox.information(
                self,
                "No selection",
                "No torrents selected."
            )

            return

        try:

            added = self.bot.add_torrents(
                selections
            )

            QMessageBox.information(
                self,
                "Success",
                f"Added {added} torrent(s)."
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )


if __name__ == "__main__":

    app = QApplication(sys.argv)

    win = MainWindow()

    win.show()

    sys.exit(app.exec())