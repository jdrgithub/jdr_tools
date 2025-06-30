import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://tutorialsdojo.com/aws-cheat-sheets/"
OUTPUT_DIR = "tutorialsdojo_cheatsheets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_cheat_sheet_links():
    resp = requests.get(BASE_URL)
    soup = BeautifulSoup(resp.text, 'html.parser')
    links = []
    for a in soup.select('a[href^="https://tutorialsdojo.com/"]'):
        href = a['href']
        if "cheat-sheet" in href and href != BASE_URL:
            links.append(href)
    return sorted(set(links))

def scrape_and_save(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    title = soup.find('h1').get_text(strip=True)
    filename = f"{title.replace(' ', '_').replace('/', '_')}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    content = [f"# {title}\n\n"]
    for tag in soup.select('h1, h2, h3, p, ul, ol, li, pre, code'):
        if tag.name.startswith('h'):
            level = int(tag.name[1])
            content.append(f"{'#' * level} {tag.get_text(strip=True)}\n\n")
        elif tag.name == 'p':
            content.append(f"{tag.get_text(strip=True)}\n\n")
        elif tag.name in ['ul', 'ol']:
            for li in tag.find_all('li'):
                content.append(f"- {li.get_text(strip=True)}\n")
            content.append("\n")
        elif tag.name in ['pre', 'code']:
            content.append(f"```\n{tag.get_text()}\n```\n\n")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(content)
    print(f"Saved: {filepath}")

if __name__ == "__main__":
    links = get_cheat_sheet_links()
    print(f"Found {len(links)} cheat sheet pages.")
    for link in links:
        scrape_and_save(link)
