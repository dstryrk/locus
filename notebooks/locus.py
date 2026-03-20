import re
import requests
from bs4 import BeautifulSoup


FILENAME = "../data/2025.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Accept-Language": "en-US,en;q=0.9",
}


def get_book_rating(book, author):
    url = "http://www.goodreads.com/search?q=" + requests.utils.quote(book + " " + author)
    page = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')
    rating = soup.find('span', class_="minirating").text
    return rating


def remove_parenthesis(string):
    return re.sub(r'\([^)]*\)', '', string)


def remove_leading_spaces(string):
    return re.sub(r'^\s+', '', string)


def return_ratings(test_string):
    # Match decimal ratings only (e.g. 3.82), avoiding bare integers like 0
    matches = re.findall(r'\d+\.\d+', test_string)
    if matches:
        return str(float(matches[0]))
    raise ValueError(f"No decimal rating found in: {test_string}")


if __name__ == "__main__":
    output_file = FILENAME.replace(".txt", ".output.txt")

    with open(FILENAME) as f:
        # Split on last comma to handle titles that contain commas
        locus = [remove_leading_spaces(remove_parenthesis(line.rstrip())).rsplit(",", 1) for line in f if line.strip()]

    results = []
    for line in locus:
        if len(line) < 2:
            continue
        title, author = line[0].strip(), line[1].strip()
        try:
            rating = return_ratings(get_book_rating(title, author))
            print(','.join([title, author, rating]))
            results.append((float(rating), ','.join([title, author, rating])))
        except:
            print(','.join([title, author, "0"]))
            results.append((0.0, ','.join([title, author, "0"])))

    results.sort(key=lambda x: x[0])
    with open(output_file, 'w') as f:
        for _, r in results:
            f.write(r + '\n')
