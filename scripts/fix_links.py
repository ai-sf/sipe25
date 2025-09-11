import os
import re
import requests
from bs4 import BeautifulSoup
import argparse

def remove_index_html_links(soup):
    # Remove "index.html" from all href attributes in <a> tags
    changed = False
    for a in soup.find_all("a", href=True):
        if "index.html" in a["href"]:
            a["href"] = a["href"].replace("index.html", "")
            changed = True
    return changed

def fix_page_id_links(soup, base_url, new_base_url):
    changed = False
    page_id_links = soup.find_all("a", href=re.compile(r"page_id=\d+"))
    for a in page_id_links:
        href = a["href"]
        match = re.search(r"page_id=(\d+)", href)
        if not match:
            continue
        page_id = match.group(1)
        test_url = f"{base_url}/?page_id={page_id}"
        try:
            r = requests.head(test_url, allow_redirects=True, timeout=5)
            final_url = r.url
            if final_url != test_url:
                if final_url.startswith(base_url):
                    final_url = final_url.replace(base_url, new_base_url, 1)
                a["href"] = final_url
                changed = True
        except Exception as e:
            print(f"Warning: Failed to fetch {test_url}: {e}")
    return changed

def fix_scrset_links(soup):
    changed = False
    for img in soup.find_all("img", srcset=True):
        del img["srcset"]
        changed = True
    return changed

def process_file(file_path, base_url, new_base_url):
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    changed = False

    changed |= remove_index_html_links(soup)
    changed |= fix_page_id_links(soup, base_url, new_base_url)
    changed |= fix_scrset_links(soup)

    if changed:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Updated {file_path}")

def main():
    parser = argparse.ArgumentParser(description="Fix links in static site HTML files.")
    parser.add_argument("root_dir", help="Root directory of the static site")
    parser.add_argument("base_url", help="Base URL of the live site (e.g., https://sipe25.com)")
    parser.add_argument("new_base_url", help="New base URL to replace old links (e.g., https://ai-sf.it/sipe)")
    args = parser.parse_args()

    for dirpath, _, filenames in os.walk(args.root_dir):
        for filename in filenames:
            if filename.endswith(".html"):
                filepath = os.path.join(dirpath, filename)
                process_file(filepath, args.base_url, args.new_base_url)

if __name__ == "__main__":
    main()
