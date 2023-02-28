import boto3
import json
import pandas as pd
import re

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
    
    df_out = pd.DataFrame.from_dict(event[0]['df_out'])
    timestamp = re.sub('/', '-', event[1]['timestamp'])
    timestamp = re.sub(' ', '_', timestamp)
    
    s3 = boto3.client('s3', aws_access_key_id = secret['id'], aws_secret_access_key= secret['key'])
    s3.put_object(Bucket='scrapedataoutput', Key=f'news-headlines-{timestamp}.csv', Body=df_out.to_csv(index=False))
    
    return None