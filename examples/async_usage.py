"""Async SDK usage — vehicle registration and web scraping."""

import asyncio

from nhvrcontrib import NHVR


async def main():
    # Pass API key directly or set NHVR_API_KEY env var
    client = NHVR()

    # --- Search regulations by topic ---
    print("=== Search: fatigue ===")
    results = await client.search("fatigue")
    print(f"Matched topic: {results.get('matched_topic')}")
    print(f"URL: {results.get('source_url')}")
    if "title" in results:
        print(f"Title: {results['title']}")

    # --- Scrape a specific page ---
    print("\n=== Scrape: mass limits page ===")
    page = await client.scrape(
        "https://www.nhvr.gov.au/road-access/mass-and-dimension/mass-limits"
    )
    print(f"Title: {page.get('title')}")
    print(f"Text preview: {page.get('text', '')[:200]}...")
    print(f"Tables found: {len(page.get('tables', []))}")
    print(f"Links found: {len(page.get('links', []))}")

    # --- Vehicle registration (requires API key) ---
    # Uncomment if you have an API key:
    # client = NHVR(api_key="your-key-here")
    # rego = await client.search_registration("ABC123")
    # print(rego)


if __name__ == "__main__":
    asyncio.run(main())
