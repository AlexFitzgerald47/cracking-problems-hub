"""
Script to perform targeted sample scraping from 1641.tcd.ie using Playwright.
Waits for the user to solve the landing CAPTCHA in a headful browser window,
then crawls a sample of deposition records (e.g. County Armagh / Cavan).
"""
import asyncio
import json
import os
import re
from playwright.async_api import async_playwright

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "sample_data.json")

async def scrape_sample(max_depositions=30):
    async with async_playwright() as p:
        print("Launching browser window (headless=False)...")
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        print("Navigating to https://1641.tcd.ie/ ...")
        await page.goto("https://1641.tcd.ie/")

        print("=== PLEASE SOLVE THE RECAPTCHA IN THE OPEN BROWSER WINDOW ===")
        # Poll until CAPTCHA is solved
        for i in range(120): # 2 minute window for human solve
            await asyncio.sleep(1)
            content = await page.content()
            current_url = page.url
            if "recaptcha" not in content.lower() and "recaptcha" not in current_url.lower():
                print(f"\n[SUCCESS] CAPTCHA passed! Reached: {current_url}")
                break
            if i % 10 == 0:
                print(f"Waiting for CAPTCHA solve... ({i}s elapsed)")
        else:
            print("[ERROR] Timed out waiting for CAPTCHA solution.")
            await browser.close()
            return

        # Navigate to search page or search for Armagh / Cavan / specific county
        print("\nNavigating to search page...")
        search_url = "https://1641.tcd.ie/search"
        await page.goto(search_url, wait_until="networkidle")
        await asyncio.sleep(2)

        content = await page.content()
        print("Search page title:", await page.title())

        # Extract links matching deposition viewer
        # Standard deposition links follow /deposition?depID=...
        links = await page.eval_on_selector_all("a[href*='deposition']", "elements => elements.map(e => e.href)")
        print(f"Found {len(links)} deposition links on initial page.")

        # If no direct links on landing search, let's submit search form or try common deposition IDs
        dep_urls = list(set(links))

        if not dep_urls:
            # Let's try browsing by volume or county if available, or try sample deposition IDs
            # Typical deposition IDs follow 810000 series (e.g., 812002, 813000, 814000, 836000, etc.)
            sample_ids = [
                "836001", "836002", "836003", "836004", "836005",
                "812002", "812003", "812004", "812005", "812006",
                "813001", "813002", "813003", "813004", "813005",
                "814001", "814002", "814003", "814004", "814005",
                "833001", "833002", "833003", "833004", "833005",
                "839001", "839002", "839003", "839004", "839005"
            ]
            dep_urls = [f"https://1641.tcd.ie/deposition?depID={did}" for did in sample_ids]

        depositions_data = []
        count = 0

        print(f"\nScraping up to {max_depositions} deposition pages...")

        for url in dep_urls:
            if count >= max_depositions:
                break
            try:
                print(f"[{count+1}/{max_depositions}] Fetching: {url}")
                await page.goto(url, wait_until="domcontentloaded")
                await asyncio.sleep(1.5)

                title = await page.title()
                html = await page.content()

                # Extract text content from main body/container
                # TCD viewer typically uses container divs or paragraphs for transcription
                text_content = await page.evaluate('''() => {
                    const el = document.querySelector('.transcription') || document.querySelector('#transcription') || document.querySelector('.content') || document.body;
                    return el ? el.innerText : '';
                }''')

                # Extract metadata fields if present
                meta = await page.evaluate('''() => {
                    const data = {};
                    document.querySelectorAll('tr, .meta-item, dl dt').forEach(row => {
                        const txt = row.innerText.trim();
                        if (txt) {
                            const parts = txt.split(/:\\s*/);
                            if (parts.length >= 2) {
                                data[parts[0].trim()] = parts.slice(1).join(': ').trim();
                            }
                        }
                    });
                    return data;
                }''')

                if text_content and len(text_content.strip()) > 50:
                    count += 1
                    depositions_data.append({
                        "id": url.split("depID=")[-1] if "depID=" in url else str(count),
                        "url": url,
                        "title": title,
                        "metadata": meta,
                        "text": text_content.strip()
                    })
                    print(f"  -> Extracted {len(text_content)} chars.")
                else:
                    print(f"  -> Skipping (empty or non-existent content).")

            except Exception as e:
                print(f"  -> Error fetching {url}: {e}")

        await browser.close()

        print(f"\nSuccessfully scraped {len(depositions_data)} depositions.")
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(depositions_data, f, indent=2, ensure_ascii=False)
        print(f"Saved sample data to {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(scrape_sample())
