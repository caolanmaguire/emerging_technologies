import requests

def get_book():
    # https://www.gutenberg.org/ebooks/84.txt.utf-8
    xy = 'https://www.gutenberg.org/ebooks/84.txt.utf-8'
    actual_book_data = requests.get(xy)
    print(actual_book_data.text)
    return 'worked'

get_book()