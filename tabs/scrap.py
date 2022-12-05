import requests
from bs4 import BeautifulSoup
from django.conf import settings
from urllib.parse import urlparse, urljoin, unquote

URL_FMT = settings.URL_FMT
HEADERS = settings.HEADERS
SCRAP_STRING_LINK_MATCH = "www.cifraclub.com.br"


def duckduckgo(search_input):
    req = requests.get(URL_FMT.format(search_input), headers=HEADERS)
    soup = BeautifulSoup(req.content)
    return [
        {"url": a.attrs.get("href"), "title": a.text}
        for a in soup.find_all("a")
        if all([a.text, a.attrs.get("href")])
    ]


def extract_tab_from_cifra_club(url):
    req = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(req.content)
    return soup.find("div", {"class": "cifra_cnt g-fix cifra-mono"})


def cifra_club_music_link(music, artist=""):
    search_term_fmt = f"{music} {artist} cifraclub"
    links = duckduckgo(search_term_fmt)

    filtered_links = []
    for link in links:
        if SCRAP_STRING_LINK_MATCH in link["url"]:
            cf_url = link["url"][link["url"].index(SCRAP_STRING_LINK_MATCH) :]
            cf_url = unquote(cf_url)
            try:
                cf_url_without_qs = cf_url[: cf_url.index("&")]
            except ValueError:
                cf_url_without_qs = cf_url
                pass
            filtered_links.append("https://" + cf_url_without_qs)
    return filtered_links


if __name__ == "__main__":
    from urllib.parse import urlparse
