import time
import re
from sources.extractor import ExtractorBase

def nbc(event, context):
    
    url = 'https://www.nbcnews.com/'
    destination = 'NBC'

    soup = ExtractorBase(url, destination)
    soup = soup.extract_by_html()

    class_dict = {'tease-card__headline':'h2',
    'styles_headline__5qvTg':'h3',
    'styles_headline__ice3t':'h2',
    'styles_baconCardsWidth':'h3',
    'related-content__headline-link':'h3',
    'cover-spread':'h2'}
    
    data = parse(soup, class_dict)
     
    return {destination: data}
    
def parse(soup, class_dict):
    lst = []    
    
    for key, value in class_dict.items():
        target = soup.find_all(value, class_=re.compile(key))
        
        for link in target:
            url = link.next_element['href']
            category = url.split('.com/')[1].split('/')[0] 
            if category == 'news':
                category = url.split('/news/')[1].split('/')[0]
            title = link.get_text(strip=True)
            title = re.sub('\xa0', ' ', title)
            lst.append([title, category])
        
    return lst