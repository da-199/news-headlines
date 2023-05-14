import psycopg2
import sys
import os
import boto3
from botocore.exceptions import ClientError
import json

def conn(event, context):

    secret_name = "postgres_connection"
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

    query_string = event['query']
    seperator = event['seperator']
    
    queries = [query for query in query_string.split(seperator) if query.strip()]
    
    try:
        conn = psycopg2.connect(host=secret['host'], port=secret['port'], database=secret['dbname'], user=secret['username'], password=secret['password'], sslrootcert="SSLCERTIFICATE")
        cur = conn.cursor()
        
        for query in queries:
            cur.execute(query)

        conn.commit()
            
    except Exception as e:
        print("Database connection failed due to {}".format(e))     
        
    conn.close()
    cur.close()    
    
    return(None)