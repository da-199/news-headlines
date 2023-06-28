from bs4 import BeautifulSoup
import requests

class ExtractorBase:

    def __init__(self, url, destination):
        self.url = url
        self.destination = destination

    def extract_by_html(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup