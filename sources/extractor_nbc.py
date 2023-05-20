import logging
import re
from typing import List

from bs4 import BeautifulSoup

from extractor_base import ExtractorBase
from models import HeadLine

class NbcExtractor(ExtractorBase):
    def __init__(self) -> None:
        self.url = 'https://www.nbcnews.com/'
        self.destination = 'NBC'
        self.class_dict = {
            'tease-card__headline':'h2',
            'styles_headline__5qvTg':'h3',
            'styles_headline__ice3t':'h2',
            'styles_baconCardsWidth':'h3',
            'related-content__headline-link':'h3',
            'cover-spread':'h2'
        }
        super().__init__()

    def extract(self):
        soup = self.extract_by_html(self.url)
        headlines = self.parse(soup)
        logging.info(f'extracted: {len(headlines)} head lines from nbc')
        return {self.destination: self.headlines_to_lists(headlines)}

    def parse(self, soup: BeautifulSoup) -> List[HeadLine]:
        headlines: List[HeadLine] = []
        for key, value in self.class_dict.items():
            target = soup.find_all(value, class_=re.compile(key))
            for link in target:
                headlines.append(self.parse_headline(link))
        return headlines

    @staticmethod
    def parse_headline(link: BeautifulSoup) -> HeadLine:
        url = link.next_element['href']
        category = url.split('.com/')[1].split('/')[0] 
        if category == 'news':
            category = url.split('/news/')[1].split('/')[0]
        title = link.get_text(strip=True)
        title = re.sub('\xa0', ' ', title)
        return HeadLine(category=category, title=title)