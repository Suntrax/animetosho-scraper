import requests
from bs4 import BeautifulSoup
from rapidfuzz import fuzz

HEADERS = {"User-Agent": "Mozilla/5.0"}


def scrape_magnet(base_url, anime):
    search_url = f"{base_url.rstrip('/')}/search?q={anime.replace(' ', '+')}"

    html = requests.get(search_url, headers=HEADERS).text
    soup = BeautifulSoup(html, "html.parser")

    best_score = 0
    best_magnet = None

    # Each result is inside this container
    entries = soup.select("div.home_list_entry")

    anime_lower = anime.lower()

    for entry in entries:
        # series name (this is what we match against)
        series_tag = entry.select_one("span.serieslink a")
        if not series_tag:
            continue

        name = series_tag.get_text(strip=True)
        name_lower = name.lower()

        score = fuzz.WRatio(anime_lower, name_lower)

        if score > best_score:
            magnet_tag = entry.select_one('a[href^="magnet:?"]')

            if magnet_tag:
                best_score = score
                best_magnet = magnet_tag["href"]

    return best_magnet


if __name__ == "__main__":
    # use anilist romaji name
    magnet = scrape_magnet(
        "https://animetosho.org/",
        "Blue Lock"
    )

    print(magnet)