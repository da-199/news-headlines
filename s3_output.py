import boto3
import json
import pandas as pd
from datetime import datetime
import dateutil.tz
from get_secrets import get_secrets

def s3_output(event, context):

    secret_name = "aws_access_key"
    secret = get_secrets(secret_name)
    
    df = pd.DataFrame()
    
    now = datetime.now()
    eastern = dateutil.tz.gettz('US/Eastern')
    timestamp = datetime.now(tz=eastern).strftime("%m-%d-%Y_%-I:%M_%p")
    
    s3 = boto3.client('s3', aws_access_key_id = secret['id'], aws_secret_access_key= secret['key'])
    s3.put_object(Bucket='news-headline-output', Key=f'news-headlines-{timestamp}.csv', Body=df.to_csv(index=False))