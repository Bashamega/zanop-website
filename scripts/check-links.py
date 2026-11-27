#!/usr/bin/env python3

import sys
import urllib.parse
import urllib.request
import urllib.error
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
IGNORED_SCHEMES = {"mailto", "tel", "javascript", "data"}
IGNORED_DOMAINS = ["gstatic.com", "googleapis.com"] # Ignore google websites


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.add(attributes["id"])
        if "name" in attributes:
            self.ids.add(attributes["name"])

        for attribute in ("href", "src"):
            if attribute in attributes:
                self.links.append((attribute, attributes[attribute]))


def read_html(path):
    parser = LinkParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def check_external(url):
    methods = ("HEAD", "GET")

    for method in methods:
        request = urllib.request.Request(
            url,
            method=method,
            headers={"User-Agent": "Mozilla/5.0 (Zanop link checker)"},
        )

        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                if response.status < 400:
                    return True
        except urllib.error.HTTPError as error:
            if error.code in (404, 410):
                return False
            if method == "HEAD":
                continue
        except (urllib.error.URLError, TimeoutError, OSError):
            continue
        except Exception:
            continue

    # Access restrictions, DNS changes, and temporary network failures are
    # not evidence that a link is broken.
    return True


broken = []
html_files = sorted(ROOT.rglob("*.html"))

for html_file in html_files:
    parser = read_html(html_file)

    for attribute, raw_link in parser.links:
        link = raw_link.strip()
        if not link or link.startswith("//"):
            continue

        parsed = urllib.parse.urlsplit(link)
        if parsed.scheme.lower() in IGNORED_SCHEMES:
            continue
        if parsed.scheme.lower() in ("http", "https"):
            hostname = (parsed.hostname or "").lower()
            if any(
                hostname == domain or hostname.endswith(f".{domain}")
                for domain in IGNORED_DOMAINS
            ):
                continue
            if not check_external(link):
                broken.append(f"{html_file.relative_to(ROOT)}: broken external {attribute}={raw_link}")
            continue
        if parsed.scheme:
            continue

        path_part = urllib.parse.unquote(parsed.path)
        if not path_part:
            target = html_file
        elif path_part.startswith("/"):
            target = (ROOT / path_part.lstrip("/")).resolve()
        else:
            target = (html_file.parent / path_part).resolve()

        try:
            target.relative_to(ROOT)
        except ValueError:
            broken.append(f"{html_file.relative_to(ROOT)}: link outside repository {attribute}={raw_link}")
            continue

        if not target.exists():
            broken.append(f"{html_file.relative_to(ROOT)}: missing {attribute}={raw_link}")
            continue

        if parsed.fragment and target.suffix.lower() == ".html":
            target_parser = read_html(target)
            if parsed.fragment not in target_parser.ids:
                broken.append(
                    f"{html_file.relative_to(ROOT)}: missing fragment #{parsed.fragment} "
                    f"in {target.relative_to(ROOT)}"
                )

if broken:
    print("Broken link detection failed:")
    for problem in broken:
        print(f"  - {problem}")
    sys.exit(1)

print(f"Checked {len(html_files)} HTML files: no broken links found")
