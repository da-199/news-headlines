import requests
import boto3
from botocore.exceptions import ClientError
import json

def nyt(event, context):

    secret_name = "nyt_api_access"
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
    key = secret['key']
    
    url = f'https://api.nytimes.com/svc/topstories/v2/home.json?api-key={key}'
    
    response = requests.get(url).json()
    
    data = []
    
    for i in response['results']:
        data.append([i['title'], i['section']])
    
    destination = 'NYT'
    
    return {destination: data}
