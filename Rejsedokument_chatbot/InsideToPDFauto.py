import asyncio
import os
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

async def run_smart_pipeline(hub_urls, project_root=None):
    # Paths
    if not project_root or not os.path.isdir(project_root):
        print(f"WARNING: The provided project_root '{project_root}' is invalid or does not exist.")
        return

    target_folder = os.path.join(project_root, "dtu_training_data")
    pdf_log_file = os.path.join(project_root, "manual_download_list.txt")
    user_session_path = os.path.join(os.getcwd(), "dtu_session")
    
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    browser_config = BrowserConfig(
        headless=False, 
        user_data_dir=user_session_path,
        use_persistent_context=True
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
        keywords = ["oekonomi", "rejser", "udgifter", "afregning"]

        # Phase 1: Scan Hubs for links
        for hub_url in hub_urls:
            print(f"Scanning Hub: {hub_url}")
            try:
                hub_result = await crawler.arun(url=hub_url, config=run_config)
                if hub_result.success:
                    links = hub_result.links.get("internal", [])
                    for link in links:
                        href = link.get("href", "")
                        if any(word in href.lower() for word in keywords) and href.startswith("http"):
                            if href.lower().endswith(".pdf"):
                                if href not in pdf_links:
                                    pdf_links.append(href)
                            elif href not in to_crawl:
                                to_crawl.append(href)
            except Exception as e:
                print(f"Hub error: {e}")

        # Save PDF list
        if pdf_links:
            with open(pdf_log_file, "w", encoding="utf-8") as f:
                f.write("--- MANUAL DOWNLOAD LIST (PDF) ---\n")
                for link in pdf_links:
                    f.write(f"{link}\n")
            print(f"LOGGED: {len(pdf_links)} PDF links saved to {pdf_log_file}")

        print(f"Found {len(to_crawl)} webpages. Starting extraction...")

        # Phase 2: Crawl webpages only
        for i, url in enumerate(to_crawl):
            url_slug = url.rstrip("/").split("/")[-1] or f"page_{i}"
            file_path = os.path.join(target_folder, f"{url_slug}.md")

            try:
                await asyncio.sleep(2) # Natural delay to help page load
                result = await crawler.arun(url=url, config=run_config)
                
                if result.success:
                    content = result.markdown.raw_markdown
                    
                    # If it looks like a 404 or empty redirect, skip it
                    if "404" in content or len(content) < 500:
                        print(f"SKIP: {url_slug} (Likely no access or 404)")
                        continue

                    header = f"# Source: {url}\n# Title: {url_slug.replace('-', ' ').title()}\n\n"
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(header + content)
                    print(f"SAVED: {url_slug}.md | Characters: {len(content)}")
                else:
                    print(f"FAIL: {url}")
            except Exception as e:
                print(f"Error on {url}: {e}")

# if __name__ == "__main__":
#     dtu_hubs = [
#         "https://www.inside.dtu.dk/oekonomi/afregning-af-udgifter-og-rejser",
#         "https://www.inside.dtu.dk/oekonomi/tjenesterejser-og-transport"
#     ]
#     project_root = r"C:\Users\botyu\OneDrive - Danmarks Tekniske Universitet\Skrivebord\Arbejde\Projekter\Rejsedokument_chatbot"
#     asyncio.run(run_smart_pipeline(dtu_hubs, project_root=project_root))