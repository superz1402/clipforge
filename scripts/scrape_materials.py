#!/usr/bin/env python3
"""Key-free stock-footage scraper for MoneyPrinterTurbo local materials.

Scrapes Mixkit's public search pages (no API key, free license) for direct
mp4 asset URLs and downloads clips.

Usage: scrape_materials.py --queries "cat,kitten" --count 5 --outdir materials
Prints downloaded file paths, one per line.
"""
import argparse
import os
import re
import sys
import urllib.request

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")


def fetch(url, dest=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    if dest:
        with open(dest, "wb") as f:
            f.write(data)
        return dest
    return data.decode("utf-8", "ignore")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--queries", required=True, help="comma-separated search terms")
    ap.add_argument("--count", type=int, default=5)
    ap.add_argument("--outdir", default="materials")
    ap.add_argument("--res", default="720")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    wanted_res = args.res.lstrip("-")
    seen_ids = set()
    downloaded = []

    for query in [q.strip() for q in args.queries.split(",") if q.strip()]:
        if len(downloaded) >= args.count:
            break
        slug = re.sub(r"[^a-z0-9]+", "-", query.lower()).strip("-")
        url = f"https://mixkit.co/free-stock-video/{slug}/"
        print(f"[search] {url}", flush=True)
        try:
            html = fetch(url)
        except Exception as exc:  # noqa: BLE001
            print(f"[search] failed: {exc}", flush=True)
            continue
        ids = re.findall(r"assets\.mixkit\.co/videos/(\d+)/", html)
        for vid in dict.fromkeys(ids):  # dedupe, keep order
            if len(downloaded) >= args.count:
                break
            if vid in seen_ids:
                continue
            seen_ids.add(vid)
            asset = f"https://assets.mixkit.co/videos/{vid}/{vid}-{wanted_res}.mp4"
            dest = os.path.join(args.outdir, f"mixkit-{vid}.mp4")
            try:
                fetch(asset, dest)
                size = os.path.getsize(dest)
                if size < 50_000:
                    os.remove(dest)
                    continue
                downloaded.append(dest)
                print(f"[ok] {asset} -> {dest} ({size // 1024} KB)", flush=True)
            except Exception as exc:  # noqa: BLE001
                print(f"[skip] {asset}: {exc}", flush=True)

    if not downloaded:
        print("ERROR: no materials downloaded", flush=True)
        sys.exit(1)
    print("---PATHS---", flush=True)
    for path in downloaded:
        print(path, flush=True)


if __name__ == "__main__":
    main()
