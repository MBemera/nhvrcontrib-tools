import httpx
from bs4 import BeautifulSoup

url = "https://www.nhvr.gov.au/road-access/mass-and-dimension/mass-limits"
html = httpx.get(url, timeout=60).text
soup = BeautifulSoup(html, "html.parser")
main = soup.find("main") or soup.body
headings = main.find_all(["h2", "h3", "h4"]) if main else []
for heading in headings[:40]:
    print(heading.name, heading.get_text(strip=True))
