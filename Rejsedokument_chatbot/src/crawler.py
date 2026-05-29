import asyncio
from pathlib import Path

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

def _is_login_page(result):
    login_url_indicators = ["login", "adfs", "signin", "microsoftonline", "auth"]
    login_content_indicators = ["sign in", "log in", "password", "microsoft account", "log på", "log ind"]

    url = (result.url or "").lower()
    if any(indicator in url for indicator in login_url_indicators):
        return True

    content = (result.markdown.raw_markdown if result.markdown else "").lower()
    if len(content) < 2000 and any(indicator in content for indicator in login_content_indicators):
        return True

    return False


async def run_smart_pipeline(hub_urls, output_dir, pdf_log_file, session_dir):
    target_folder = Path(output_dir)
    pdf_log_file = Path(pdf_log_file)
    user_session_path = Path(session_dir)

    target_folder.mkdir(parents=True, exist_ok=True)
    pdf_log_file.parent.mkdir(parents=True, exist_ok=True)
    user_session_path.mkdir(parents=True, exist_ok=True)

    browser_config = BrowserConfig(
        headless=False,
        user_data_dir=str(user_session_path),
        use_persistent_context=True,
    )

    # Simplified Generator
    md_generator = DefaultMarkdownGenerator(
        options={
            "bypass_tables": False,
            "ignore_links": True,
            "ignore_images": True,
            "strip_lines": True,
            "remove_comments": True
        }
    )

    # Basic RunConfig - Removed delay_before_return_crops
    run_config = CrawlerRunConfig(
        markdown_generator=md_generator,
        process_iframes=True,
        cache_mode=CacheMode.BYPASS,
        wait_until="networkidle"
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        # --- LOGIN PHASE ---
        print("\n!!! ACTION REQUIRED !!!")
        print("Checking login status. If the browser shows the login page, please log in.")
        print("Once you see the actual content, press ENTER in this terminal.")
        
        await crawler.arun(url=hub_urls[0], config=run_config)
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, input, "Press ENTER after you have verified the page is loaded...")

        to_crawl = []
        pdf_links = []
        # keywords = ["oekonomi", "afregning", "rejser", "udgifter", "transport", "kørsel", "taxa", "kreditkort", "CWT", "fly", "afregning", "godtgørelse"]
        keywords = ["transport", "kørsel", "taxa","CWT", "tjenesterejse", "flyforsinkelse", "Lavprisfly", "rejseforsikringskort", "transport", "brobizz", "parkering"]
        # Phase 1: Scan Hubs for links
        for hub_url in hub_urls:
            print(f"Scanning Hub: {hub_url}")
            try:
                hub_result = await crawler.arun(url=hub_url, config=run_config)
                if hub_result.success:
                    links = hub_result.links.get("internal", [])
                    for link in links:
                        href = link.get("href", "")
                        text = link.get("text", "").lower()
                        if any(word in href.lower() or word in text for word in keywords) and href.startswith("http"):
                            if href.lower().endswith(".pdf"):
                                if href not in pdf_links:
                                    pdf_links.append(href)
                            elif href not in to_crawl:
                                to_crawl.append(href)
            except Exception as e:
                print(f"Hub error: {e}")

        print(f"Found {len(to_crawl)} webpages. Starting BFS extraction...")

        # Phase 2: BFS crawl — follow sub-links that stay within each hub's own section
        hub_prefixes = [h.rstrip("/") + "/" for h in hub_urls]
        visited = set(to_crawl)
        queue = list(to_crawl)
        i = 0

        while queue:
            url = queue.pop(0)
            url_slug = url.rstrip("/").split("/")[-1] or f"page_{i}"
            file_path = target_folder / f"{url_slug}.md"

            try:
                await asyncio.sleep(2)
                result = await crawler.arun(url=url, config=run_config)

                if result.success and _is_login_page(result):
                    print(f"\n!!! LOGIN REQUIRED: {url_slug} redirected to a login page.")
                    print("Please log in in the browser window, then press ENTER to retry...")
                    await loop.run_in_executor(None, input, "Press ENTER after logging in...")
                    result = await crawler.arun(url=url, config=run_config)

                if result.success:
                    content = result.markdown.raw_markdown

                    if "404" in content or len(content) < 500:
                        print(f"SKIP: {url_slug} (Likely no access or 404)")
                    else:
                        header = f"# Source: {url}\n# Title: {url_slug.replace('-', ' ').title()}\n\n"
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(header + content)
                        print(f"SAVED: {url_slug}.md | Characters: {len(content)}")

                        # Queue sub-links that stay within the hub URL scope
                        for link in result.links.get("internal", []):
                            href = link.get("href", "")
                            if not href.startswith("http") or href in visited:
                                continue
                            if any(href.startswith(prefix) for prefix in hub_prefixes):
                                if href.lower().endswith(".pdf"):
                                    if href not in pdf_links:
                                        pdf_links.append(href)
                                else:
                                    queue.append(href)
                                    visited.add(href)
                else:
                    print(f"FAIL: {url}")
            except Exception as e:
                print(f"Error on {url}: {e}")
            i += 1

        # Save PDF list (after BFS so PDFs found during sub-crawl are included)
        if pdf_links:
            with open(pdf_log_file, "w", encoding="utf-8") as f:
                f.write("--- MANUAL DOWNLOAD LIST (PDF) ---\n")
                for link in pdf_links:
                    f.write(f"{link}\n")
            print(f"LOGGED: {len(pdf_links)} PDF links saved to {pdf_log_file}")
