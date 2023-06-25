import boto3
import json
import pandas as pd
import re
from datetime import datetime
import dateutil.tz

def s3_output(event, context):

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
    
    df = pd.DataFrame(event)
    
    now = datetime.now()
    eastern = dateutil.tz.gettz('US/Eastern')
    timestamp = datetime.now(tz=eastern).strftime("%m-%d-%Y_%-I:%M_%p")
    
    s3 = boto3.client('s3', aws_access_key_id = secret['id'], aws_secret_access_key= secret['key'])
    s3.put_object(Bucket='news-headline-output', Key=f'news-headlines-{timestamp}.csv', Body=df.to_csv(index=False))
    
    return None