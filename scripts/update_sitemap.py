#!/usr/bin/env python3

import subprocess
import sys
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from urllib.parse import urljoin


def get_last_modified(file_path: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", str(file_path)],
            check=True,
            capture_output=True,
            text=True,
        )
        if result.stdout.strip():
            return result.stdout.strip()
    except subprocess.CalledProcessError:
        pass

    timestamp = file_path.stat().st_mtime
    return datetime.fromtimestamp(timestamp, timezone.utc).isoformat()


def get_domain(root: Path) -> str:
    cname = root / "CNAME"
    if cname.is_file():
        domain = cname.read_text(encoding="utf-8").strip()
        if domain:
            return domain
    return "example.com"


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    domain = get_domain(root)
    base_url = f"https://{domain}/"

    pages = [
        path
        for path in sorted(root.rglob("*.html"))
        if ".git" not in path.parts
        and "node_modules" not in path.parts
        and path.name.lower() != "404.html"
    ]

    entries = []
    for path in pages:
        relative = path.relative_to(root).as_posix()
        if relative == "index.html":
            route = ""
        elif relative.endswith("/index.html"):
            route = relative[: -len("index.html")]
        elif relative.endswith(".html"):
            route = relative[: -len(".html")]
        else:
            route = relative

        location = urljoin(base_url, route)
        last_modified = get_last_modified(path)
        priority = "1.0000" if relative == "index.html" else "0.6400"
        entries.append(
            f"""  <url>
    <loc>{escape(location)}</loc>
    <lastmod>{escape(last_modified)}</lastmod>
    <priority>{priority}</priority>
  </url>"""
        )

    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )
    (root / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
