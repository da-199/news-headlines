from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd
from datetime import datetime

driver = webdriver.Safari()
url = "http://www.bloomberg.com"
driver.get(url)

headline = driver.find_elements(By.CLASS_NAME, 'single-story-module__headline-link')
related =  driver.find_elements(By.CLASS_NAME, 'single-story-module__related-story-link')
pkgHeadline = driver.find_elements(By.CLASS_NAME, 'story-package-module__story__headline-link')
headlineLink = driver.find_elements(By.CLASS_NAME, 'story-list-story__info__headline-link')

data = []

for i in headlineLink:
    data.append(i.text)
    
for k in pkgHeadline:
    data.append(k.text)
    
for j in related:
    data.append(j.text)
    
for l in headline:
    data.append(l.text)

driver.quit()
   
lst = [re.sub('\s\s+', '', i,) for i in data]
lst = list(set(lst))
df = pd.DataFrame(lst)
now = datetime.now()
df['Datetime'] = now.strftime("%m/%d/%Y %-I:%M:%S")
df = df.rename(columns={df.columns[0]: "Title"})
df['Source'] = 'Bloomberg Main Section'
