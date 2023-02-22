import time
import re
from bs4 import BeautifulSoup
import requests

def nbc(event, context):
    
    url = 'https://www.nbcnews.com/'
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')

	class_dict = {'tease-card__headline':'h2',
	'styles_headline__5qvTg':'h3',
	'styles_headline__ice3t':'h2',
	'styles_baconCardsWidth':'h3',
	'related-content__headline-link':'a',
	'cover-spread':'h2'}
    
    data = parse(class_dict)
    
    destination = 'NBC'
    
    return {'data': data, 'destination': destination}
    
def parse(class_dict):
    final = []    
    
    for key, value in class_dict.items():
        lst = [x.get_text(strip=True) for x in soup.find_all(value, class_=re.compile(key))]
        final.extend(lst)
        
    return final

