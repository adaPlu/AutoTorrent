# torrentbot.py — version 1.4
# Author: Adam Pluguez
# Date: 2025-07-16
# License: This code is free to use and modify under the MIT License.

import requests
from bs4 import BeautifulSoup
from transmission_rpc import Client, TransmissionAuthError
from urllib.parse import unquote, parse_qs, urlparse


class TorrentBot:
    def __init__(
        self,
        host,
        port,
        user,
        password,
        download_dir,
        site_url="https://piratebay.party"
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.download_dir = download_dir
        self.site_url = site_url.rstrip('/')

    def search_magnets_with_pagination(self, query, limit=999):
        found = []
        debug_log = []
        page = 0

        while len(found) < limit:

            url = (
                f"{self.site_url}/search/"
                f"{requests.utils.quote(query)}/{page}/99/0"
            )

            try:
                r = requests.get(url, timeout=10)
                r.raise_for_status()
            except Exception as e:
                debug_log.append(
                    f"Request failed on page {page}: {e}"
                )
                break

            soup = BeautifulSoup(r.text, "html.parser")
            rows = soup.find_all("tr")

            if not rows:
                break

            for row in rows:

                magnet_tag = row.find(
                    "a",
                    href=True,
                    title="Download this torrent using magnet"
                )

                if not magnet_tag:
                    continue

                magnet_href = magnet_tag["href"]

                if not magnet_href.startswith("magnet:"):
                    continue

                parsed = urlparse(magnet_href)
                qs = parse_qs(parsed.query)

                raw_title = qs.get("dn", [None])[0]
                title = (
                    unquote(raw_title)
                    if raw_title
                    else "Unknown Title"
                )

                # Extract seeders
                seeders = 0

                try:
                    cols = row.find_all("td")

                    if len(cols) >= 7:
                        seeders = int(
                            cols[5].get_text(strip=True)
                        )
                except Exception:
                    pass

                found.append(
                    (
                        title,
                        magnet_href,
                        seeders
                    )
                )

                debug_log.append(
                    f"SEEDERS: {seeders}\n"
                    f"TITLE: {title}\n"
                    f"MAGNET: {magnet_href}\n"
                )

                if len(found) >= limit:
                    break

            page += 1

        # Sort highest seeders first
        found.sort(
            key=lambda x: x[2],
            reverse=True
        )

        with open(
            "debug_parse_log.txt",
            "w",
            encoding="utf-8"
        ) as f:
            f.write("\n\n".join(debug_log))

        return found

    def search_magnets(self, query, limit=99):

        url = (
            f"{self.site_url}/search/"
            f"{requests.utils.quote(query)}/0/99/0"
        )

        r = requests.get(url, timeout=10)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        found = []
        debug_log = []

        for row in soup.find_all("tr"):

            magnet_tag = row.find(
                "a",
                href=True,
                title="Download this torrent using magnet"
            )

            if not magnet_tag:
                continue

            magnet_href = magnet_tag["href"]

            if not magnet_href.startswith("magnet:"):
                continue

            parsed = urlparse(magnet_href)
            qs = parse_qs(parsed.query)

            raw_title = qs.get("dn", [None])[0]
            title = (
                unquote(raw_title)
                if raw_title
                else "Unknown Title"
            )

            seeders = 0

            try:
                cols = row.find_all("td")

                if len(cols) >= 7:
                    seeders = int(
                        cols[5].get_text(strip=True)
                    )
            except Exception:
                pass

            found.append(
                (
                    title,
                    magnet_href,
                    seeders
                )
            )

            debug_log.append(
                f"SEEDERS: {seeders}\n"
                f"TITLE: {title}\n"
                f"MAGNET: {magnet_href}\n"
            )

            if len(found) >= limit:
                break

        found.sort(
            key=lambda x: x[2],
            reverse=True
        )

        with open(
            "debug_parse_log.txt",
            "w",
            encoding="utf-8"
        ) as f:
            f.write("\n\n".join(debug_log))

        return found

    def add_torrents(self, selections):

        try:
            client = Client(
                host=self.host,
                port=self.port,
                username=self.user,
                password=self.password
            )

        except TransmissionAuthError:
            raise Exception(
                "Transmission authentication failed."
            )

        added = 0

        for title, link, seeders in selections:

            try:
                client.add_torrent(
                    link,
                    download_dir=self.download_dir
                )
                added += 1

            except Exception as e:
                print(
                    f"Failed to add {title}: {e}"
                )

        return added