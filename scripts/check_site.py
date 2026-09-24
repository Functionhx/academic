#!/usr/bin/env python3
"""Check a built academic site: pages, languages, local links, leftovers."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit

REQUIRED_PAGES = {"index.html": "en", "zh/index.html": "zh"}
REQUIRED_ANCHORS = ("about-me", "news", "publications", "research")
FORBIDDEN_TEXT = (
    "Lorem ipsum",
    "RayeRen/acad-homepage.github.io/google-scholar-stats",
    "500x300.png",
    "googletagmanager.com/gtag/js?id=\"",  # analytics loaded without an id
)
# The built stylesheet must carry the dark palette (explicit choice and the
# no-JavaScript system fallback) and honour reduced motion.
REQUIRED_CSS = ("html[data-theme=dark]", "prefers-color-scheme:dark", "prefers-reduced-motion:reduce")
SKIP_SCHEMES = {"http", "https", "mailto", "tel", "javascript", "data"}


class Collector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[str] = []
        self.ids: set[str] = set()
        self.lang: str | None = None
        self.canonical: str | None = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        if a.get("id"):
            self.ids.add(a["id"])
        for key in ("href", "src"):
            if a.get(key):
                self.refs.append(a[key])


def resolve(site: Path, baseurl: str, page: Path, ref: str) -> Path | None:
    parts = urlsplit(ref)
    if parts.scheme in SKIP_SCHEMES or (not parts.path and parts.fragment):
        return None
    path = unquote(parts.path)
    if path.startswith("/"):
        if baseurl and not (path == baseurl or path.startswith(baseurl + "/")):
            return site / "__outside_baseurl__" / path.lstrip("/")
        path = path[len(baseurl):] if baseurl else path
        target = site / path.lstrip("/")
    else:
        target = page.parent / path
    if target.is_dir() or path.endswith("/"):
        target = target / "index.html"
    return target


def check(site: Path, baseurl: str) -> list[str]:
    problems: list[str] = []
    for rel, lang in REQUIRED_PAGES.items():
        if not (site / rel).is_file():
            problems.append(f"missing page: {rel}")
    for page in sorted(site.rglob("*.html")):
        text = page.read_text(encoding="utf-8")
        rel = page.relative_to(site).as_posix()
        for bad in FORBIDDEN_TEXT:
            if bad in text:
                problems.append(f"{rel}: leftover template text {bad!r}")
        c = Collector()
        c.feed(text)
        if rel in REQUIRED_PAGES and c.lang != REQUIRED_PAGES[rel]:
            problems.append(f"{rel}: html lang={c.lang!r}, expected {REQUIRED_PAGES[rel]!r}")
        if rel in REQUIRED_PAGES:
            for anchor in REQUIRED_ANCHORS:
                if anchor not in c.ids:
                    problems.append(f"{rel}: missing section anchor #{anchor}")
            want = f"{baseurl}/{rel.removesuffix('index.html')}"
            if c.canonical is None or urlsplit(c.canonical).path != want:
                problems.append(f"{rel}: canonical {c.canonical!r} should have path {want!r}")
            if "tech-blog-link" not in c.ids:
                problems.append(f"{rel}: missing Tech Blog link")
            if "theme-toggle" not in c.ids:
                problems.append(f"{rel}: missing theme toggle")
            if 'localStorage.getItem("theme")' not in text:
                problems.append(f"{rel}: theme is not applied before first paint")
            if 'class="page__footer-credit"' not in text or "github.com/RayeRen/acad-homepage.github.io" not in text:
                problems.append(f"{rel}: MIT template credit missing")
        for ref in c.refs:
            parts = urlsplit(ref)
            if not parts.scheme and not parts.path and parts.fragment and parts.fragment not in c.ids:
                problems.append(f"{rel}: anchor #{parts.fragment} has no target")
            target = resolve(site, baseurl, page, ref)
            if target is not None and not target.exists():
                problems.append(f"{rel}: broken local ref {ref}")
    css = site / "assets/css/main.css"
    css_text = "".join(css.read_text(encoding="utf-8").split()) if css.is_file() else ""
    for needle in REQUIRED_CSS:
        if needle.replace(" ", "") not in css_text:
            problems.append(f"assets/css/main.css: missing {needle!r}")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("site", type=Path)
    ap.add_argument("--baseurl", default="")
    args = ap.parse_args()
    problems = check(args.site, args.baseurl.rstrip("/"))
    for p in problems:
        print(p)
    print(f"{'FAIL' if problems else 'OK'}: {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
