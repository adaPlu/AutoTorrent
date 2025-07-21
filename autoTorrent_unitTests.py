# autoTorrent_unitTests.py
# Author: Adam Pluguez
# Date: 2025-07-16
# A collection of basic unit tests for autoTorrent.
# License: This code is free to use and modify under the MIT License.

import pytest
from torrentbot import TorrentBot
from unittest.mock import MagicMock, patch
from urllib.parse import urlparse, parse_qs, unquote


@pytest.fixture
def torrentbot(tmp_path):
    return TorrentBot(
        host="dummy", port=9091, user="user", password="pass",
        download_dir=str(tmp_path), site_url="https://example.com"
    )


def test_add_torrents_success(torrentbot):
    with patch("torrentbot.Client") as MockClient:
        mock_client = MockClient.return_value
        mock_client.add_torrent = MagicMock()

        selections = [("Ubuntu", "magnet:?xt=urn:btih:abc"), ("Debian", "magnet:?xt=urn:btih:def")]
        added = torrentbot.add_torrents(selections)

        assert added == 2
        assert mock_client.add_torrent.call_count == 2

def test_add_torrents_auth_fail(torrentbot, capsys):
    with patch("torrentbot.Client") as MockClient:
        mock_client = MockClient.return_value
        mock_client.add_torrent.side_effect = Exception("authentication failed")

        selections = [("BadTorrent", "magnet:?xt=urn:btih:fail")]
        count = torrentbot.add_torrents(selections)

        captured = capsys.readouterr()
        assert "Failed to add BadTorrent: authentication failed" in captured.out
        assert count == 0

def test_parse_title_from_magnet():
    magnet = "magnet:?xt=urn:btih:123&dn=Star+Trek+Voyager"
    parsed = urlparse(magnet)
    qs = parse_qs(parsed.query)
    title = unquote(qs.get("dn", ["Unknown Title"])[0])
    assert title == "Star Trek Voyager"


def test_search_url_format():
    bot = TorrentBot("h", 1, "u", "p", "/tmp")
    query = "ubuntu"
    url = f"{bot.site_url}/search/{query}/0/99/0"
    assert url.endswith("/search/ubuntu/0/99/0")
