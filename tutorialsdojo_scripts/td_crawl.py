import os
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

BASE_URL = "https://tutorialsdojo.com/aws-cheat-sheets/"
OUTPUT_DIR = "tutorialsdojo_cheatsheets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_cheat_sheet_links_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True later for full headless
        page = browser.new_page()
        print(f"Loading index page: {BASE_URL}")
        page.goto(BASE_URL)
        page.wait_for_timeout(5000)

        html = page.content()
        with open('index_page_dump.html', 'w', encoding='utf-8') as f:
            f.write(html)
        browser.close()

        soup = BeautifulSoup(html, 'html.parser')
        links = []

        # Find AWS Cheat Sheets menu block
        aws_menu_root = None
        for li in soup.select('li.menu-item'):
            anchor = li.find('a')
            if anchor and 'AWS Cheat Sheets' in anchor.get_text():
                aws_menu_root = li
                break

        if aws_menu_root:
            for a in aws_menu_root.select('ul.sub-menu a[href^="https://tutorialsdojo.com/"]'):
                href = a['href']
                links.append(href)

        print(f"Filtered {len(links)} AWS Cheat Sheet links.")
        return sorted(set(links))

def scrape_and_save(browser, url):
    try:
        page = browser.new_page()
        print(f"Scraping: {url}")
        page.goto(url)
        html = page.content()
        page.close()

        soup = BeautifulSoup(html, 'html.parser')
        h1 = soup.find('h1')
        if h1 is None:
            print(f"Skipping {url}: No H1 title found.")
            return

        title = h1.get_text(strip=True)
        filename = f"{title.replace(' ', '_').replace('/', '_')}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)

        content = [f"# {title}\n\n"]

        # Find the "Last updated on" marker (now handles nested tags like <strong>)
        start_tag = soup.find(lambda tag: tag.name == 'p' and "last updated on" in tag.get_text(strip=True).lower())

        if not start_tag:
            print(f"Skipping {url}: Couldn't find 'Last updated on' marker.")
            return

        # Start collecting content from the next siblings after the marker
        for tag in start_tag.next_siblings:
            if getattr(tag, 'name', None) in ['footer', 'nav'] or \
               (getattr(tag, 'get', lambda x: None)('id') in ['footer', 'site-footer']):
                break

            if not getattr(tag, 'name', None):
                continue  # Skip text nodes, comments, etc.

            text = tag.get_text(strip=True)
            if not text:
                continue

            if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                level = int(tag.name[1])
                content.append(f"{'#' * level} {text}\n\n")
            elif tag.name == 'p':
                content.append(f"{text}\n\n")
            elif tag.name in ['ul', 'ol']:
                for li in tag.find_all('li'):
                    content.append(f"- {li.get_text(strip=True)}\n")
                content.append("\n")
            elif tag.name in ['pre', 'code']:
                content.append(f"```\n{tag.get_text()}\n```\n\n")
            elif tag.name in ['div', 'section', 'span']:
                content.append(f"{text}\n\n")

        if len(content) > 1:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(content)
            print(f"Saved: {filepath}")
        else:
            print(f"Skipping {url}: No content collected after marker.")

    except Exception as e:
        print(f"Error scraping {url}: {e}")

if __name__ == "__main__":
    links = get_cheat_sheet_links_playwright()
    print(f"\nFound {len(links)} AWS Cheat Sheet pages.\n")

    with open('cheatsheet_urls.txt', 'w') as f:
        f.write('\n'.join(links))

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            for link in links:
                scrape_and_save(browser, link)
    except KeyboardInterrupt:
        print("\nScraping interrupted by user. Exiting gracefully.")
