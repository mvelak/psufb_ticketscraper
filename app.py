import flask

from errors import scrapingError
from scrape import scrape_listings
from utils import filter_listings
from database import check_for_unsaved_listings, overwrite_saved_listings

app = flask.Flask(__name__)

@app.route('/')
def index():
    try:
        listings = scrape_listings()
    except scrapingError:   # Early exits
        return 'No Data', 500    # 500 Internal Server Error

    args = flask.request.args   # Dictionary of argument keys and their values

    if len(args.keys()) > 0:
        listings = filter_listings(listings, args)

    res = {'listings': listings}
    return res, 200  # 200 OK


@app.route('/update', methods=['POST'])
def update():
    try:
        listings = scrape_listings()
    except scrapingError:
        return 'no data', 500

    unsaved_listings = check_for_unsaved_listings(listings)

    overwrite_saved_listings(listings)

    res = {'new_listings': unsaved_listings}
    return res, 200

app.run(debug=True)