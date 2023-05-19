

from sources.extractor_nbc import NbcExtractor
from bs4 import BeautifulSoup

def test_parse_headline():

    with open("test_nbc.html") as test_file:
        soup = BeautifulSoup(test_file, 'html.parser')
        headlines = NbcExtractor().parse(soup)
        print(headlines)