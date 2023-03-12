import re
from bs4 import BeautifulSoup
import requests

def abc(event, context):
    
    url = 'https://abcnews.go.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    class_dict = {'News__title':'h4',
    'News__Item__Headline':'h2',
    'title':'div',
    'FirstVideo__Title':'div',
    'ListItem__Title':'div',
    'VideoTile__Title':'h3'}
    
    data = []
    
    destination = 'ABC'
    
    for key, value in class_dict.items():
        
        target = soup.find_all(value, class_=key)
        
        for x in target:
    
            if key == 'News__title':
                title = x.get_text(strip=True)
                url = x.parent.get('href')
                category = url.split('/')[3].lower()  
                data.append([title, category])
    
            if key == 'News__Item__Headline':
                title = x.get_text(strip=True)    
                url = x.previous_element.previous_element.get('href')
                category = url.split('/')[3].lower()
                data.append([title, category])
    
            if key == 'title':
                title = x.next_element.get_text(strip=True)    
                url = x.next_element.get('href')
                category = url.split('/')[3].lower()
                data.append([title, category])
    
            if key == 'FirstVideo__Title':           
                title = x.get_text(strip=True)   
                data.append([title, category])  
    
            if key == 'ListItem__Title':
                title = x.next_element.get_text(strip=True)    
                url = x.next_element.get('href')
                category = url.split('/')[3].lower()   
                data.append([title, category])
    
            if key == 'VideoTile__Title':
                title = x.get_text(strip=True)    
                url = x.parent.get('href')
                if url is not None:
                    category = url.split('/')[3].lower()
                else:
                    category = 'none'
                data.append([title, category])             
        
    return {destination: data}
    