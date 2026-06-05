import re
from urllib.parse import urljoin, urlsplit

def _filename(url: str) -> str:
    return urlsplit(url).path.rsplit("/", 1)[-1]

def pick_from_master(master_text: str, master_url: str, quality: str) -> str:
    variants = []  # (bandwidth, url)
    lines = master_text.splitlines()
    bw = None
    for line in lines:
        line = line.strip()
        if line.startswith("#EXT-X-STREAM-INF"):
            m = re.search(r"BANDWIDTH=(\d+)", line)
            bw = int(m.group(1)) if m else 0
        elif line and not line.startswith("#"):
            variants.append((bw or 0, urljoin(master_url, line)))
            bw = None
    if not variants:
        raise ValueError("no variants in master playlist")
    if quality == "highest":
        return max(variants, key=lambda v: v[0])[1]
    for _, url in variants:
        if quality in _filename(url):
            return url
    raise ValueError(f"quality {quality} not found in master")

def _bitrate_in_url(url: str) -> int:
    m = re.search(r"(\d+)k\.m3u8", url)
    return int(m.group(1)) if m else 0

def pick_from_urls(urls: list[str], quality: str) -> str:
    if quality == "highest":
        return max(urls, key=_bitrate_in_url)
    for url in urls:
        if quality in _filename(url):
            return url
    raise ValueError(f"quality {quality} not found in captured urls: {urls}")
