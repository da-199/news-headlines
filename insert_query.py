import re
import pandas as pd
from datetime import datetime
import dateutil.tz
import boto3
from botocore.exceptions import ClientError
import json

def insert_query(event, context):
    
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
    
    df_out = pd.DataFrame()

    for source in event:
        data = source['data']
        destination = source['destination']
        dest_table = 'headline'
    
        if destination == 'NBC':
            data = [re.sub(r"'", '’', i,) for i in data]
    
        data = list(set(data))
    
        df = pd.DataFrame(data)
        now = datetime.now()
        eastern = dateutil.tz.gettz('US/Eastern')
        df['Datetime'] = datetime.now(tz=eastern).strftime("%m/%d/%Y %-I:%M %p")
        df = df.rename(columns={df.columns[0]: "Title"})
        df['Source'] = destination
        df_out = pd.concat([df, df_out])
        
    s3 = boto3.client('s3', aws_access_key_id = secret['id'], aws_secret_access_key= secret['key'])
    s3.put_object(Bucket='scrapedataoutput', Key='nbc_data.csv', Body=df_out.to_csv(index=False))
    
    insert = """
    INSERT INTO public.{dest_table} (
        """.format(dest_table=dest_table)
    
    columns_string = str(list(df_out.columns))[1:-1]
    columns_string = re.sub(r' ', '\n        ', columns_string)
    columns_string = re.sub(r'\'', '', columns_string)
    
    values_string = ''
    
    for row in df_out.itertuples(index=False,name=None):
        row = re.sub(r'"', "'", str(row))
        values_string += re.sub(r'nan', 'null', str(row))
        values_string += ',\n'
    
    delete_statement = f"DELETE FROM {dest_table} WHERE DATETIME < NOW() - INTERVAL '1 DAY'"
    
    query = insert + columns_string + ')\n     VALUES\n' + values_string[:-2] + ';' + '\n' + delete_statement + ';'
    
    return {'query': query}
