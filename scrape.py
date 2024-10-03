import requests, re
from bs4 import BeautifulSoup
from errors import scrapingError


# Decode cloudflare email encryption
def _decode_email(code: str) -> str:
    r = int(code[:2], 16)
    decoded_email = "".join([chr(int(code[i : i + 2], 16) ^ r) for i in range(2, len(code), 2)])
    return decoded_email


def scrape_listings():
    # Ensure that we can establish a connection to the site
    req = requests.get('https://onwardstate.com/penn-state-football-student-ticket-exchange/')
    if req.status_code != 200:
        raise scrapingError

    soup = BeautifulSoup(req.content, 'html.parser')
    listings = []

    for pgraph in soup.find_all('p'):
        pgraph = str(pgraph)
        match = re.search('data-cfemail="(.*)"', pgraph)
        if match is not None:
            email = _decode_email(match.group(1))
            match = re.search(r"wants (.*) for a (.*) \(.*\) ticket.", pgraph)
            price, game = match.group(1), match.group(2)
            info = {'email': email, 'game': game, 'price': price}
            listings.append(info)

    return listings