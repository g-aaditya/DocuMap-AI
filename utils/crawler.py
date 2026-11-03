import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import tldextract
from utils.logger import info, warn

def crawl(start_url, max_depth, max_pages):
    visited = set()
    pages = []
    domain = tldextract.extract(start_url).registered_domain

    def dfs(url, depth):
        if depth > max_depth or len(visited) >= max_pages or url in visited:
            return
        try:
            info(f"Crawling: {url}")
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                return
        except:
            warn(f"Failed to fetch {url}")
            return

        visited.add(url)
        soup = BeautifulSoup(r.text, "html.parser")
        pages.append((url, soup))

        for link in soup.find_all("a", href=True):
            next_url = urljoin(url, link["href"])
            if domain in urlparse(next_url).netloc:
                dfs(next_url, depth + 1)

    dfs(start_url, 0)
    return pages
