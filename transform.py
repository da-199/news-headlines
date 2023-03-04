import re
import pandas as pd
from datetime import datetime
import dateutil.tz
import boto3
import json

def transform(event, context):
    
    cat_dict = {'tech':'technology', 'us':'us-news', 'select':'shopping'}
    
    df_out = pd.DataFrame()

    for source in event:
        [destination] = source.keys()
        [source] = source.values() 
        dest_table = 'headline'
    
        if destination == 'NBC':
            for i in source:
                i[0] = re.sub(r"'", '’', str(i[0]))
    
        df = pd.DataFrame(source)
        now = datetime.now()
        eastern = dateutil.tz.gettz('US/Eastern')
        df['Datetime'] = datetime.now(tz=eastern).strftime("%m/%d/%Y %-I:%M %p")
        df = df.rename(columns={df.columns[0]: "Title", df.columns[1]: "Category"})
        df['Source'] = destination
        df_out = pd.concat([df, df_out])
    
    for key, value in cat_dict.items():
        df_out['Category'].loc[df_out['Category']==key] = value
    
    df_out['Category'] = df_out['Category'].apply(lambda x: 'other' if x.count('-')>=3 else x)
    
    df_out = df_out[['Title', 'Datetime', 'Source', 'Category']]  
    
    s3_output(df_out, df['Datetime'].max())    
        
    return {'dest_table': dest_table}, {'df_out': df_out.to_dict('list')}
    
def s3_output(df_out, timestamp):

    secret_name = "aws_access_key"
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
        
    secret = get_secret_value_response['SecretString']
    secret = json.loads(secret)
    
    timestamp = re.sub('/', '-', timestamp)
    timestamp = re.sub(' ', '_', timestamp)
    
    s3 = boto3.client('s3', aws_access_key_id = secret['id'], aws_secret_access_key= secret['key'])
    s3.put_object(Bucket='scrapedataoutput', Key=f'news-headlines-{timestamp}.csv', Body=df_out.to_csv(index=False))
    
    return None