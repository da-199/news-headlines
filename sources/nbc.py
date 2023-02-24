import time
import re
import requests
from bs4 import BeautifulSoup

def nbc(event, context):
    
    url = 'https://www.nbcnews.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    class_dict = {'tease-card__headline':'h2',
    'styles_headline__5qvTg':'h3',
    'styles_headline__ice3t':'h2',
    'styles_baconCardsWidth':'h3',
    'related-content__headline-link':'h3',
    'cover-spread':'h2'}
    
    data = parse(soup, class_dict)
    
    destination = 'NBC'
    
    return {destination: data}
    
def parse(soup, class_dict):
    lst = []    
    
    for key, value in class_dict.items():
        target = soup.find_all(value, class_=re.compile(key))
        
        for link in target:
            url = link.next_element['href']
            category = url.split('.com/')[1].split('/')[0]   
            title = link.get_text(strip=True)
            lst.append([title, category])
        
    return lst