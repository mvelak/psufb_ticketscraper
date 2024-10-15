import json

database_file = 'listings.txt'
def serialize_listing(listing):
    return json.dumps(listing, sort_keys=True, indent=4)


def unserialized_line(line):
    return json.loads(line)


def _read_database():
    lines = []

    try:
        with open(database_file, 'r') as f:
            for line in f.readlines():      # array of all lines
                lines.append(line.strip())
    except FileNotFoundError:
        pass

    return lines


def get_saved_listings():
    saved_lines = _read_database()
    saved_listings = map(unserialized_line, saved_lines)
    return saved_listings


def check_for_unsaved_listings(listings):
    saved_lines = _read_database()
    saved_lines = set(saved_lines)

    unsaved_listings = []
    for listing in listings:
        line = serialize_listing(listing)

        if line not in saved_lines:
            unsaved_listings.append(line)

    return unsaved_listings


def overwrite_saved_listings(listings):
    listings = map(lambda l: serialize_listing(l) + '\n', listings)

    with open(database_file, 'w') as f:
        f.writelines(listings)
