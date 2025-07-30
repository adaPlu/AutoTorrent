# AutoTorrent

_AutoTorrent_ is a lightweight, Python-based GUI application that allows you to search for torrents on The Pirate Bay and send magnet links directly to your local Transmission client with one click. Designed for ease of use, AutoTorrent supports customizable search limits, connection settings, and integrates seamlessly with PyQt6 and Transmission RPC.

---

## 🔧 Features

- ✅ **Magnet link search** via [The Pirate Bay](https://piratebay.party)
- ✅ **Auto-extract torrent titles** from magnet links
- ✅ **Send selected torrents** directly to Transmission
- ✅ **Customizable settings** (host, port, username, password, download directory, search result limit)
- ✅ **Dark-mode friendly PyQt6 UI**
- ✅ **Debug logging** and HTML fallback
- ✅ 🧪 Basic unit test suite (`pytest`)
- ✅ 🧱 Portable `.exe` builds supported via PyInstaller

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/autoTorrent.git
cd autoTorrent
2. Install Dependencies
Create a virtual environment (optional but recommended):

bash
Copy
Edit
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
requirements.txt
txt
Copy
Edit
PyQt6
requests
beautifulsoup4
transmission-rpc
pytest
🖥️ Usage
Run the GUI:
bash
Copy
Edit
python gui.py
⚙️ Configure Transmission:
On first launch, click Settings and enter your:
Local Transmission server Settings:

Host: //192.168.X.XXX/

Port: 9091

Username: transmission

Password: transmission

Local Download Dir: //192.168.X.XXX/*.*/

Current Max Results: 1–999

✅ Search & Download
Enter a query (e.g., Star Trek)

Select desired torrents

Click Add Selected to send to Transmission

📦 Build to EXE (Optional)
AutoTorrent works well with PyInstaller for packaging.

bash
Copy
Edit
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed gui.py
Your executable will appear in the /dist folder.

⚠️ If using PyQt6: you may need to manually copy platforms/qwindows.dll into dist/platforms/.

🧪 Unit Testing
Run included unit tests:

bash
Copy
Edit
pytest test_torrentbot_gui.py
🔍 Known Issues
Some search results may fail to extract titles if Pirate Bay HTML changes

Requires Transmission to be running and reachable on LAN

GUI is Windows-optimized; Linux/macOS not yet tested

📜 License
MIT License
Copyright (c) 2025 Adam Pluguez
See LICENSE for full terms.

🙋‍♀️ Contact
Built with ❤️ by Adam Pluguez
📧 Email: adapluguez@gmail.com
🔗 GitHub: github.com/adaPlu

💡 Future Plans
 Add support for alternate torrent search engines
 Dark theme toggle & UI themes
