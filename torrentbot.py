# torrentbot.py — version 1.3
# Author: Adam Pluguez
# Date: 2025-07-16
# License: This code is free to use and modify under the MIT License.
import requests
from bs4 import BeautifulSoup
from transmission_rpc import Client, TransmissionAuthError
from urllib.parse import unquote, parse_qs, urlparse
class TorrentBot:
    def __init__(self, host, port, user, password, download_dir, site_url="https://piratebay.party"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.download_dir = download_dir
        self.site_url = site_url.rstrip('/')

    # Main search method that extracts titles from magnet link (dn= param)
    def search_magnets(self, query, limit=25):
        url = f"{self.site_url}/search/{requests.utils.quote(query)}/0/99/0"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        found = []
        debug_log = []

        for row in soup.find_all("tr"):
            magnet_tag = row.find("a", href=True, title="Download this torrent using magnet")
            if not magnet_tag:
                continue

            magnet_href = magnet_tag['href']
            if not magnet_href.startswith("magnet:"):
                continue

            # Extract torrent title from dn= query parameter
            parsed = urlparse(magnet_href)
            qs = parse_qs(parsed.query)
            raw_title = qs.get("dn", [None])[0]
            title = unquote(raw_title) if raw_title else "Unknown Title"

            found.append((title, magnet_href))
            debug_log.append(f"TITLE: {title}\nMAGNET: {magnet_href}\n")

            if len(found) >= limit:
                break
        # Save parsed results to debug log - For changes in html structure
        with open("debug_parse_log.txt", "w", encoding="utf-8") as f:
            f.write("\n\n".join(debug_log))

        return found

    # Add selected torrents to Transmission
    def add_torrents(self, selections):
        try:
            client = Client(host=self.host, port=self.port,
                            username=self.user, password=self.password)
        except TransmissionAuthError:
            raise Exception("Transmission authentication failed.")
        added = 0
        for title, link in selections:
            try:
                client.add_torrent(link, download_dir=self.download_dir)
                added += 1
            except Exception as e:
                print(f"Failed to add {title}: {e}")
        return added
