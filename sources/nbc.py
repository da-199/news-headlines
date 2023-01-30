from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def nbc(event, context):
    options = Options()
    options.binary_location = '/opt/headless-chromium'
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument("--disable-extensions")
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome('/opt/chromedriver', chrome_options=options)
    
    url = "https://www.nbcnews.com/"
    driver.get(url)
    
    data = []

    head = driver.find_elements(By.CLASS_NAME, 'tease-card__headline')
    relatedHead = driver.find_elements(By.CLASS_NAME, 'related-content__headline-link')
    subhead = driver.find_elements(By.CSS_SELECTOR, "[class^=styles_headline__5qvTg]")
    baconCards = driver.find_elements(By.CSS_SELECTOR, "[class^=styles_baconCardsWidthByOneHeader]")
    iceHead = driver.find_elements(By.CLASS_NAME, 'styles_headline__ice3t')
    cs = driver.find_elements(By.CSS_SELECTOR, "[class^=cover-spread__headline]")
    cst = driver.find_elements(By.CLASS_NAME, 'cover-spread-tease__headline-link')
    
    for a in cs:
        data.append(a.text)
        
    for b in cst:
        data.append(b.text)
    
    for c in baconCards:
        data.append(c.text)
        
    for d in iceHead:
        data.append(d.text)
    
    for e in head:
        data.append(e.text)    
    
    for l in relatedHead:
        data.append(l.text)
        
    for j in subhead:
        data.append(j.text)

    driver.quit()
    
    data = list(filter(None, data))
    destination = 'NBC'
    
    return {'data': data, 'destination': destination}
