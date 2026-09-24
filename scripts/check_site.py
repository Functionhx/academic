#!/usr/bin/env python3
"""Check a built academic site: pages, languages, local links, leftovers."""

from __future__ import annotations

import argparse
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit

REQUIRED_PAGES = {"index.html": "en", "zh/index.html": "zh"}
REQUIRED_ANCHORS = ("about-me", "news", "publications", "research", "education")
# Per-page localisation of the browser title, share metadata, and language alternates.
PAGE_META = {
    "index.html": {"title": "Yuchen Fan", "og_locale": "en_US", "research": "/research/3d-scene-intelligence/"},
    "zh/index.html": {"title": "樊宇琛", "og_locale": "zh_CN", "research": "/research/3d-scene-intelligence/"},
}
# Owner decision 2026-09-24: both hosts and both languages link the Chinese blog on github.io.
BLOG_ORIGIN = "https://functionhx.github.io"
SCHOLAR_URL = "https://scholar.google.com/citations?user=xxUw0bkAAAAJ"
# sha256 of the acad-homepage template's own icons (verified byte-identical to
# RayeRen/acad-homepage.github.io main); shipping them shows someone else's mark.
TEMPLATE_FAVICON_HASHES = {
    "e31942e7fcb3a09df25dead1bca3419b7a3b3483430ec91425ea11362a5397ea",  # favicon-16x16.png
    "89dd48e8d2923b2ea66ff4f9e2361dacf24d52787ba4eb239d210cb13e3de112",  # favicon-32x32.png
    "0cd14aea27a1f23e355281dbfd0b4dc1b4e388131179e5994078e4f3b36eabff",  # apple-touch-icon.png
}
FORBIDDEN_TEXT = (
    "Lorem ipsum",
    "RayeRen/acad-homepage.github.io/google-scholar-stats",
    "500x300.png",
    "googletagmanager.com/gtag/js?id=\"",  # analytics loaded without an id
    # Owner decision 2026-09-24: nothing about the double-blind submission
    # appears until it is accepted.
    "instance image goal navigation",
    "实例图像目标导航",
    "under review",
    "在投",
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
        self.meta: dict[str, str] = {}
        self.alternates: dict[str, str] = {}
        self.icons: list[str] = []
        self.jsonld: list[str] = []
        self.title = ""
        self._in: str | None = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        if tag == "link" and a.get("rel") == "alternate" and a.get("hreflang"):
            self.alternates[a["hreflang"]] = a.get("href", "")
        if tag == "link" and a.get("rel") == "icon":
            self.icons.append(a.get("href", ""))
        if tag == "meta" and (a.get("name") or a.get("property")):
            self.meta[a.get("name") or a.get("property")] = a.get("content", "")
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in = "jsonld"
            self.jsonld.append("")
        if tag == "title":
            self._in = "title"
        if a.get("id"):
            self.ids.add(a["id"])
        for key in ("href", "src"):
            if a.get(key):
                self.refs.append(a[key])

    def handle_endtag(self, tag):
        if tag in ("script", "title"):
            self._in = None

    def handle_data(self, data):
        if self._in == "jsonld":
            self.jsonld[-1] += data
        elif self._in == "title":
            self.title += data


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


def check_meta(c: Collector, text: str, rel: str, baseurl: str) -> list[str]:
    want = PAGE_META[rel]
    problems: list[str] = []
    if want["title"] not in c.title:
        problems.append(f"browser title {c.title.strip()!r} should contain {want['title']!r}")
    if c.meta.get("og:locale") != want["og_locale"]:
        problems.append(f"og:locale {c.meta.get('og:locale')!r}, expected {want['og_locale']!r}")
    for key in ("description", "og:description", "og:image"):
        if not c.meta.get(key):
            problems.append(f"missing meta {key}")
    if c.meta.get("og:image") and not c.meta["og:image"].startswith("https://"):
        problems.append("og:image must be an absolute https URL")
    alt_paths = {lang: urlsplit(href).path for lang, href in c.alternates.items()}
    expected_alts = {"en": f"{baseurl}/", "zh-CN": f"{baseurl}/zh/", "x-default": f"{baseurl}/"}
    if alt_paths != expected_alts:
        problems.append(f"hreflang alternates {alt_paths}, expected {expected_alts}")
    people = []
    for block in c.jsonld:
        try:
            data = json.loads(block)
        except ValueError:
            problems.append("JSON-LD does not parse")
            continue
        if data.get("@type") == "Person":
            people.append(data)
    if len(people) != 1:
        problems.append("expected exactly one JSON-LD Person")
    elif not any(u.startswith(SCHOLAR_URL) for u in people[0].get("sameAs", [])):
        problems.append("JSON-LD Person sameAs lacks Google Scholar")
    for r in c.refs:
        host = urlsplit(r).netloc
        if host == "fanyuchen.com.cn" or (host == "functionhx.github.io" and urlsplit(r).path.startswith("/en/")):
            problems.append(f"blog link {r} must go to the Chinese blog on {BLOG_ORIGIN}")
    if SCHOLAR_URL not in text:
        problems.append("Google Scholar profile link missing")
    if f"{BLOG_ORIGIN}{want['research']}" not in c.refs:
        problems.append(f"Research does not link the blog page {want['research']}")
    return problems


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
            problems.extend(f"{rel}: {p}" for p in check_meta(c, text, rel, baseurl))
            if 'class="page__footer-credit"' not in text or "github.com/RayeRen/acad-homepage.github.io" not in text:
                problems.append(f"{rel}: MIT template credit missing")
        for ref in c.refs:
            parts = urlsplit(ref)
            if not parts.scheme and not parts.path and parts.fragment and parts.fragment not in c.ids:
                problems.append(f"{rel}: anchor #{parts.fragment} has no target")
            target = resolve(site, baseurl, page, ref)
            if target is not None and not target.exists():
                problems.append(f"{rel}: broken local ref {ref}")
    for icon in ("images/favicon-16x16.png", "images/favicon-32x32.png", "images/apple-touch-icon.png"):
        f = site / icon
        if f.is_file() and hashlib.sha256(f.read_bytes()).hexdigest() in TEMPLATE_FAVICON_HASHES:
            problems.append(f"{icon}: still the template's icon")
    manifest = site / "images/site.webmanifest"
    if manifest.is_file():
        data = json.loads(manifest.read_text(encoding="utf-8"))
        if not data.get("name"):
            problems.append("images/site.webmanifest: empty name")
        for icon in data.get("icons", []):
            if not (manifest.parent / icon["src"]).is_file():
                problems.append(f"images/site.webmanifest: icon {icon['src']!r} does not resolve")
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
