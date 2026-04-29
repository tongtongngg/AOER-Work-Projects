import asyncio
import os
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import json

async def run_smart_pipeline(base_url, project_root=None):

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

    md_generator = DefaultMarkdownGenerator(
        options={
            "bypass_tables": False,
            "ignore_links": True,
            "ignore_images": True,
            "strip_lines": True,
            "remove_comments": True
        }
    )

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
        

        await crawler.arun(url=base_url, config=run_config)
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, input, "Press ENTER after you have verified the page is loaded...")

        formatted_cookies = {}
        try:
            # 1. Get the browser object from the strategy
            browser = crawler.crawler_strategy.browser
            
            if browser and browser.contexts:
                # 2. Grab cookies from the first context
                # (Since you're using use_persistent_context, this is where your login lives)
                playwright_cookies = await browser.contexts[0].cookies()
                formatted_cookies = {c['name']: c['value'] for c in playwright_cookies}
                print(f"Successfully captured {len(formatted_cookies)} session cookies.")
            else:
                print("Warning: Browser context not found. PDFs might not download correctly.")
        except Exception as e:
            print(f"Error extracting cookies: {e}")
            print("The script will continue, but PDF downloads might fail if authentication is required.")

        # --- HIERARCHICAL CRAWL PHASE ---
        visited = set()
        queue = [base_url]
        pdf_links = []
        
        print(f"\nStarting hierarchical crawl from: {base_url}")
        
        while queue:
            current_url = queue.pop(0)
            
            # Skip if we've already scraped this page
            if current_url in visited:
                continue
                
            visited.add(current_url)
            
            # Create a safe filename from the URL
            url_slug = current_url.rstrip("/").split("/")[-1] or "index"
            file_path = os.path.join(target_folder, f"{url_slug}.md")
            
            print(f"Crawling: {current_url}")
            
            try:
                await asyncio.sleep(2) # Natural delay to help page load
                result = await crawler.arun(url=current_url, config=run_config)
                
                if result.success:
                    content = result.markdown.raw_markdown
                    
                    # If it looks like a 404 or empty redirect, skip it
                    if "404" in content or len(content) < 500:
                        print(f"  -> SKIP: {url_slug} (Likely no access or 404)")
                        continue

                    # Save the page text
                    header = f"# Source: {current_url}\n# Title: {url_slug.replace('-', ' ').title()}\n\n"
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(header + content)
                    print(f"  -> SAVED: {url_slug}.md | Characters: {len(content)}")
                    
                    # Find deeper links to scrape
                    links = result.links.get("internal", [])
                    
                    # Define words or paths you want to completely ignore
                    ignore_paths = ["/covid-19"] 
                    
                    for link in links:
                        # Get the link and strip out any anchor tags
                        href = link.get("href", "").split('#')[0]
                        
                        # NEW: If the link contains any of our ignored paths, skip it entirely
                        if any(ignored in href.lower() for ignored in ignore_paths):
                            continue
                        
                        # 1. Is it a PDF? Grab it regardless of where it is hosted!
                        if href.lower().endswith(".pdf"):
                            if href not in pdf_links:
                                pdf_links.append(href)
                        
                        # 2. Is it a web page? Only queue it if it's deeper in our specific hierarchy
                        elif href.startswith(base_url) and href not in visited and href not in queue:
                            queue.append(href)
                else:
                    print(f"  -> FAIL: {current_url}")
            except Exception as e:
                print(f"  -> Error on {current_url}: {e}")

        # Save PDF list
        if pdf_links:
            with open(pdf_log_file, "w", encoding="utf-8") as f:
                f.write("--- MANUAL DOWNLOAD LIST (PDF) ---\n")
                for link in pdf_links:
                    f.write(f"{link}\n")
            print(f"\nLOGGED: {len(pdf_links)} PDF links saved to {pdf_log_file}")
            
        print(f"\nCrawl complete! Processed {len(visited)} pages.")

        return formatted_cookies # <--- Add this
