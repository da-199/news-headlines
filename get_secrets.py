import boto3
import json

def get_secrets(secret_name):

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

    return secret