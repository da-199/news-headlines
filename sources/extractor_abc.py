import re
from bs4 import BeautifulSoup
import requests

import logging
import re
from typing import List

from bs4 import BeautifulSoup

from extractor_base import ExtractorBase
from models import HeadLine

class AbcExtractor(ExtractorBase):
    def __init__(self) -> None:
        self.url = 'https://abcnews.go.com/'
        self.destination = 'ABC'
        self.class_dict = {
            'News__title':'h4',
            'News__Item__Headline':'h2',
            'title':'div',
            'FirstVideo__Title':'div',
            'ListItem__Title':'div',
            'VideoTile__Title':'h3'
        }
    
        super().__init__()
    def extract(self):
        soup = self.extract_by_html(self.url)
        headlines = self.parse(soup)
        logging.info(f'extracted: {len(headlines)} head lines from abc')
        return {self.destination: self.headlines_to_lists(headlines)}

    def parse(self, soup: BeautifulSoup) -> List[HeadLine]:

        headlines: List[HeadLine] = []
        for key, value in self.class_dict.items():
            target = soup.find_all(value, class_=key)
            for x in target:
                headlines.append(self.parse_headline(key, x))
        return headlines
    @staticmethod
    def parse_headline(key:str, x: BeautifulSoup) -> HeadLine:
        if key == 'News__title':
            title = x.get_text(strip=True)
            url = x.parent.get('href')
            category = url.split('/')[3].lower()
            return HeadLine(category=category, title=title)

        if key == 'News__Item__Headline':
            title = x.get_text(strip=True)    
            url = x.previous_element.previous_element.get('href')
            category = url.split('/')[3].lower()
            return HeadLine(category=category, title=title)

        if key == 'title':
            title = x.next_element.get_text(strip=True)    
            url = x.next_element.get('href')
            category = url.split('/')[3].lower()
            return HeadLine(category=category, title=title)

        if key == 'FirstVideo__Title':           
            title = x.get_text(strip=True)
            # TODO is this a bug???
            category = 'N/A' 
            return HeadLine(category=category, title=title)

        if key == 'ListItem__Title':
            title = x.next_element.get_text(strip=True)    
            url = x.next_element.get('href')
            category = url.split('/')[3].lower()
            return HeadLine(category=category, title=title)

        if key == 'VideoTile__Title':
            title = x.get_text(strip=True)    
            url = x.parent.get('href')
            if url is not None:
                category = url.split('/')[3].lower()
            else:
                category = 'none' # using None here might be better?
            return HeadLine(category=category, title=title)
    