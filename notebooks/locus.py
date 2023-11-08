import re

# write a method that searches for a book and author in goodreads and returns the book's rating
import requests
from bs4 import BeautifulSoup

def get_book_rating(book, author):
    url = "https://www.goodreads.com/search?q=" + book + "+" + author
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    rating = soup.find('span', class_="minirating").text
    return rating

## write a method that removes the text between two parenthesis, including the parenthesis in python
def remove_parenthesis(string):
    return re.sub(r'\([^)]*\)', '', string)

## write a method that removes the leading spaces in python
def remove_leading_spaces(string):
    return re.sub(r'^\s+', '', string)

filename = "../data/2022.txt"
with open(filename) as f:
    # for each line in the file, remove the parenthesis and leading spaces, then return the part before the comma and the part after teh comma
    locus = [remove_leading_spaces(remove_parenthesis(line.rstrip())).split(",") for line in f]

## write a method that returns the first number in a sting 
def return_ratings(test_string):
    #digits = [i for i in test_string.split() if i.isdigit()]
    return str(float(re.findall(r"[-+]?\d*\.\d+|\d+", test_string)[0]))

for line in locus:
    try:
        rating = return_ratings(get_book_rating(line[0], line[1]))
        print (','.join([line[0],line[1].strip(),rating]))
    except:
        print (','.join([line[0],line[1].strip(),"0"]))