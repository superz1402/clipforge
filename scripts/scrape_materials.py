#!/usr/bin/env python3
"""Key-free stock-footage scraper for MoneyPrinterTurbo local materials.

Two no-API-key sources, tried in order per query:
1. Mixkit search pages (free license, direct mp4 assets) - modern stock look,
   but thin libraries for specific animals.
2. Internet Archive (public-domain / CC-BY nature footage, e.g. NOAA Ocean
   Exploration) - deep archive, license-filtered for monetization safety
   (no NC/ND). Attribution lines land in <outdir>/credits.txt.

Usage: scrape_materials.py --queries "cat,kitten" --count 5 --outdir materials
Prints downloaded file paths, one per line.
"""
import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

MAX_ARCHIVE_BYTES = 90_000_000  # skip full-length videos
ALLOWED_LICENSE = ("publicdomain", "licenses/by/", "licenses/by-sa")


def fetch(url, dest=None):
    # No retries on 429: when a source throttles us we stop and fall back,
    # we don't keep hitting it.
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = resp.read()
    if dest:
        with open(dest, "wb") as f:
            f.write(data)
        return dest
    return data


def mixkit_ids(query):
    slug = re.sub(r"[^a-z0-9]+", "-", query.lower()).strip("-")
    url = f"https://mixkit.co/free-stock-video/{slug}/"
    print(f"[mixkit] {url}", flush=True)
    html = fetch(url).decode("utf-8", "ignore")
    ids = re.findall(r"assets\.mixkit\.co/videos/(\d+)/", html)
    return list(dict.fromkeys(ids))


def archive_items(query):
    # Title-search the subject noun inside trusted public-domain nature
    # collections (NOAA Ocean Exploration). Unscoped archive.org search
    # returns description-matched junk and unsafe uploads, so stay narrow.
    noun = query.split()[0] if query.split() else query
    q = urllib.parse.urlencode({
        "q": f"title:({noun}) AND mediatype:movies AND collection:(hessel-digital-library)",
        "fl[]": ["identifier", "title", "licenseurl", "downloads"],
        "rows": "15",
        "sort[]": "downloads desc",
        "output": "json",
    }, doseq=True)
    url = f"https://archive.org/advancedsearch.php?{q}"
    print(f"[archive] {url}", flush=True)
    data = json.loads(fetch(url))
    docs = data.get("response", {}).get("docs", [])
    ok = []
    for d in docs:
        # Only NOAA Ocean Exploration uploads: other agencies in the
        # collection (e.g. National Park Service) mix in B&W historical
        # and visitor footage that fails topic matching.
        if not d.get("identifier", "").startswith("noaa-oe-video"):
            continue
        lic = (d.get("licenseurl") or "").lower()
        if any(a in lic for a in ALLOWED_LICENSE) and "nc" not in lic and "nd" not in lic:
            ok.append(d)
    return ok


def archive_best_file(identifier):
    data = json.loads(fetch(f"https://archive.org/metadata/{identifier}"))
    best = None
    for f in data.get("files", []):
        name = f.get("name", "")
        if not name.lower().endswith((".mp4", ".mkv", ".mov")):
            continue
        size = int(f.get("size") or 0)
        if size < 500_000 or size > MAX_ARCHIVE_BYTES:
            continue
        length = float(f.get("length") or 0)
        if length and length < 4:
            continue
        if best is None or size < best[1]:
            best = (name, size)
    meta = data.get("metadata", {})
    return best, meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--queries", required=True, help="comma-separated search terms")
    ap.add_argument("--count", type=int, default=5)
    ap.add_argument("--outdir", default="materials")
    ap.add_argument("--res", default="720")
    ap.add_argument("--prefix", default="", help="filename prefix (e.g. 01- for ordered beats)")
    ap.add_argument("--source", default="auto", choices=["auto", "mixkit", "archive"])
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    wanted_res = args.res.lstrip("-")
    used_file = os.path.join(args.outdir, ".used_ids")
    seen_ids = set()
    if os.path.exists(used_file):
        seen_ids.update(x.strip() for x in open(used_file) if x.strip())
    credits_path = os.path.join(args.outdir, "credits.txt")
    downloaded = []
    new_ids = []

    def save(dest, asset, credit):
        try:
            fetch(asset, dest)
            size = os.path.getsize(dest)
            if size < 50_000:
                os.remove(dest)
                return False
            downloaded.append(dest)
            new_ids.append(credit.split("\t")[0])
            print(f"[ok] {asset} -> {dest} ({size // 1024} KB)", flush=True)
            with open(credits_path, "a") as cf:
                cf.write(credit + "\n")
            return True
        except Exception as exc:  # noqa: BLE001
            print(f"[skip] {asset}: {exc}", flush=True)
            return False

    queries = [q.strip() for q in args.queries.split(",") if q.strip()]

    if args.source in ("auto", "mixkit"):
        for query in queries:
            if len(downloaded) >= args.count:
                break
            try:
                for vid in mixkit_ids(query):
                    if len(downloaded) >= args.count:
                        break
                    if f"mixkit-{vid}" in seen_ids:
                        continue
                    asset = f"https://assets.mixkit.co/videos/{vid}/{vid}-{wanted_res}.mp4"
                    dest = os.path.join(args.outdir, f"{args.prefix}mixkit-{vid}.mp4")
                    save(dest, asset, f"mixkit-{vid}\tMixkit (Free License)\t{asset}")
            except Exception as exc:  # noqa: BLE001
                print(f"[mixkit] failed: {exc}", flush=True)

    for query in queries:
        if len(downloaded) >= args.count:
            break
        if args.source in ("auto", "archive"):
            try:
                for item in archive_items(query):
                    if len(downloaded) >= args.count:
                        break
                    ident = item["identifier"]
                    if f"archive-{ident}" in seen_ids:
                        continue
                    best, meta = archive_best_file(ident)
                    if not best:
                        print(f"[archive] no usable file in {ident}", flush=True)
                        continue
                    fname, _ = best
                    asset = f"https://archive.org/download/{ident}/{urllib.parse.quote(fname)}"
                    dest = os.path.join(args.outdir, f"{args.prefix}archive-{ident}.mp4")
                    title = meta.get("title", ident)
                    lic = meta.get("licenseurl", "")
                    creator = meta.get("creator", "")
                    if isinstance(creator, list):
                        creator = ", ".join(creator)
                    save(dest, asset,
                         f"archive-{ident}\t{title}\t{creator}\t{lic}\thttps://archive.org/details/{ident}")
            except Exception as exc:  # noqa: BLE001
                print(f"[archive] failed: {exc}", flush=True)

    if new_ids:
        with open(used_file, "a") as f:
            f.write("\n".join(new_ids) + "\n")

    if not downloaded:
        print("ERROR: no materials downloaded", flush=True)
        sys.exit(1)
    print("---PATHS---", flush=True)
    for path in downloaded:
        print(path, flush=True)


if __name__ == "__main__":
    main()
