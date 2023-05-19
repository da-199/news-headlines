import logging
import requests
from bs4 import BeautifulSoup
from typing import Any, Dict, List, Tuple
from models import HeadLine
class ExtractorBase:

    def load_key():
        pass
    def extract_by_html(self, target_url: str) -> BeautifulSoup:
        logging.debug(f'fetching: {target_url}')
        response = requests.get(target_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def extract_by_json():
        pass
    def extract(input_url) -> Dict[str, Any]:
        pass

    @staticmethod
    def headlines_to_lists(headlines: List[HeadLine]) -> List[Tuple[str]]: 
        return [[headline.title, headline.category] for headline in headlines]