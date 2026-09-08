"""
Full Corpus Downloader for the 1641 Depositions (1641.tcd.ie).
Iterates across all 33 manuscript volumes (MS 809 to MS 841), extracts all deposition IDs,
and downloads the complete transcribed text corpus into `all_depositions.json`.

Supply the authenticated session cookie locally through the `DEPOSITIONS_COOKIE`
environment variable. Never commit a browser cookie to this repository.
"""
import argparse
import json
import os
import re
import time
import urllib.request
from bs4 import BeautifulSoup

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "all_depositions.json")
PROGRESS_FILE = os.path.join(os.path.dirname(__file__), "crawl_progress.json")

# Manuscript volumes MS 809 through MS 841 (33 volumes)
MANUSCRIPT_IDS = [str(ms) for ms in range(809, 842)]

def make_request(url, cookie_str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": cookie_str
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8", errors="ignore")

def crawl_corpus(cookie_str, max_depositions=None):
    print("Starting 1641 Depositions Corpus Retrieval...")

    scraped_data = {}
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                scraped_data = json.load(f)
            print(f"Loaded {len(scraped_data)} previously downloaded depositions from checkpoint.")
        except Exception as e:
            print(f"Could not load checkpoint: {e}")

    dep_urls_to_fetch = set()

    print("\nPhase 1: Discovering all deposition IDs across Manuscript Volumes (MS 809 - MS 841)...")
    for ms_id in MANUSCRIPT_IDS:
        page = 1
        max_pages = 1
        print(f"Scanning Manuscript MS {ms_id}...")

        while page <= max_pages:
            url = f"https://1641.tcd.ie/browse/searchResults/?sort=folio_start,%20manuscript_number&dir=asc&msID={ms_id}&StartAge=0&sort=manuscript_number&dir=desc&page={page}"
            try:
                html = make_request(url, cookie_str)
                soup = BeautifulSoup(html, "html.parser")

                # Find pagination links to determine total pages for this MS
                pag_links = soup.find_all("a", href=re.compile(r"page=\d+"))
                for link in pag_links:
                    m = re.search(r"page=(\d+)", link["href"])
                    if m:
                        p_num = int(m.group(1))
                        if p_num > max_pages:
                            max_pages = p_num

                # Extract deposition links
                dep_links = soup.find_all("a", href=re.compile(r"deposition\?depID="))
                for link in dep_links:
                    href = link["href"]
                    m = re.search(r"depID=([a-zA-Z0-9]+)", href)
                    if m:
                        dep_id = m.group(1)
                        full_url = f"https://1641.tcd.ie/deposition?depID={dep_id}"
                        dep_urls_to_fetch.add((dep_id, full_url))

                print(f"  MS {ms_id} (Page {page}/{max_pages}): Found {len(dep_links)} deposition links. Total unique: {len(dep_urls_to_fetch)}")
                page += 1
                time.sleep(0.2)

            except Exception as e:
                print(f"  Error fetching search page MS {ms_id} p{page}: {e}")
                break

    all_deps_list = sorted(list(dep_urls_to_fetch), key=lambda x: x[0])
    print(f"\nPhase 1 Complete: Discovered {len(all_deps_list)} unique deposition records across all 33 volumes.")

    if max_depositions:
        all_deps_list = all_deps_list[:max_depositions]
        print(f"Capping download to first {max_depositions} depositions as requested.")

    print(f"\nPhase 2: Downloading deposition transcriptions...")
    count = 0
    total = len(all_deps_list)

    for dep_id, url in all_deps_list:
        count += 1
        if dep_id in scraped_data:
            continue

        try:
            html = make_request(url, cookie_str)
            soup = BeautifulSoup(html, "html.parser")

            title = soup.title.string.strip() if soup.title else f"Deposition {dep_id}"

            # Extract metadata from table if present
            meta = {}
            for row in soup.find_all("tr"):
                cells = row.find_all(["td", "th"])
                if len(cells) >= 2:
                    k = cells[0].get_text(strip=True)
                    v = cells[1].get_text(strip=True)
                    if k and v:
                        meta[k] = v

            # Extract full transcribed text from all itemContent divs
            item_contents = soup.find_all(class_="itemContent")
            if item_contents:
                text_content = "\n\n".join([item.get_text("\n", strip=True) for item in item_contents])
            else:
                text_div = soup.find(class_=re.compile(r"transcription|content|deposition-text", re.I))
                text_content = text_div.get_text("\n", strip=True) if text_div else soup.get_text("\n", strip=True)

            scraped_data[dep_id] = {
                "id": dep_id,
                "url": url,
                "title": title,
                "metadata": meta,
                "text": text_content
            }

            if count % 20 == 0 or count == total:
                print(f"[{count}/{total}] Downloaded deposition {dep_id} ({len(text_content)} chars). Total saved: {len(scraped_data)}")

            # Save checkpoint every 50 records
            if len(scraped_data) % 50 == 0:
                with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
                    json.dump(scraped_data, f, indent=2, ensure_ascii=False)

            time.sleep(0.15)

        except Exception as e:
            print(f"  Error fetching deposition {dep_id}: {e}")

    # Final Save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(scraped_data, f, indent=2, ensure_ascii=False)
    print(f"\nSUCCESS! Completed download of {len(scraped_data)} depositions. Saved to {OUTPUT_FILE}")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--max-depositions",
        type=int,
        help="optional cap for a diagnostic partial crawl",
    )
    args = parser.parse_args()
    cookie_str = os.environ.get("DEPOSITIONS_COOKIE")
    if not cookie_str:
        parser.error("set DEPOSITIONS_COOKIE in the local environment before crawling")
    crawl_corpus(cookie_str, max_depositions=args.max_depositions)


if __name__ == "__main__":
    main()
