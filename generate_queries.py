import re
from datetime import datetime
import dateutil.tz
import boto3
from botocore.exceptions import ClientError
import json
import pandas as pd

def generate_queries(event, context):
    
    [df] = event.values()
    [dest_table] = event.keys()
    df = pd.DataFrame(df)
    
    insert = """
    INSERT INTO public.{dest_table} (
        """.format(dest_table=dest_table)
    
    columns_string = str(list(df.columns))[1:-1]
    columns_string = re.sub(r' ', '\n        ', columns_string)
    columns_string = re.sub(r'\'', '', columns_string)
    
    values_string = ''
    
    for row in df.itertuples(index=False,name=None):
        row = re.sub(r'"', "'", str(row))
        values_string += re.sub(r'nan', 'null', str(row))
        values_string += ',\n'
    
    query = insert + columns_string + ')\n     VALUES\n' + values_string[:-2] + ';' + '\n' + ';'
    
    return {'query': query}