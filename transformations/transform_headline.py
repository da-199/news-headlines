import re
import pandas as pd
from datetime import datetime
import dateutil.tz
import boto3
import json

def headline_table(event, context):
    df_headline = parse_input(event)
    df_headline = transform_date(df_headline)
    df_headline = transform_title(df_headline)
    df_headline = transform_category(df_headline)
    return df_headline.to_dict('list')
    
def parse_input(event):
    df_headline = pd.DataFrame()
    dest_table = 'v2_headline'
    
    for source in event:

        [destination] = source.keys()
        [data_source] = source.values() 
        
        df = pd.DataFrame(data_source)
        df['Source'] = destination
        df_headline = pd.concat([df, df_headline])
    return df_headline
    
def transform_date(df_headline):
    now = datetime.now()
    eastern = dateutil.tz.gettz('US/Eastern')
    df_headline['Datetime'] = datetime.now(tz=eastern).strftime("%m/%d/%Y %-I:%M %p")
    return df_headline
    
def transform_category(df_headline):
    df_headline = df_headline.rename(columns={df_headline.columns[1]: "Category"})
    
    cat_dict = {'tech':'technology',
    'us':'us-news',
    'select':'shopping',
    'international':'world'} 

    for key, value in cat_dict.items():
        df_headline['Category'].loc[df_headline['Category']==key] = value
        
    df_headline['Category'] = df_headline['Category'].apply(lambda x: 'other' if x.count('-')>=3 else x) 
    df_headline['Category'].loc[df_headline['Category']=='abcnews'] = 'none'
    return df_headline

def transform_title(df_headline):
    df_headline = df_headline.rename(columns={df_headline.columns[0]: "Title"})
    df_headline['Title'] = df_headline['Title'].apply(lambda x: x.replace("'", "''").replace("’", "''"))
    df_headline['Title'] = df_headline['Title'].apply(lambda x: x.replace(";", ":"))
    return df_headline