import flask

from errors import scrapingError
from scrape import scrape_listings

app = flask.Flask(__name__)

@app.route('/')
def index():
    try:
        listings = scrape_listings()
        res = {'listings': listings}
        return res, 200     # 200 OK
    except scrapingError:
        return 'No Data', 500    # 500 Internal Server Error

app.run(debug=True)