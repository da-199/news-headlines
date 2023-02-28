import re
import pandas as pd
from datetime import datetime
import dateutil.tz
import boto3
from botocore.exceptions import ClientError
import json

def insert_query(event, context):
    
    cat_dict = {'tech':'technology', 'us':'us-news', 'select':'shopping'}
    
    df_out = pd.DataFrame()

    for source in event:
        [data] = list(source.values())
        [destination] = source.keys()
        dest_table = 'headline'
    
        if destination == 'NBC':
            for i in data:
                i[0] = re.sub(r"'", '’', str(i[0]))
    
        df = pd.DataFrame(data)
        now = datetime.now()
        eastern = dateutil.tz.gettz('US/Eastern')
        df['Datetime'] = datetime.now(tz=eastern).strftime("%m/%d/%Y %-I:%M %p")
        df = df.rename(columns={df.columns[0]: "Title", df.columns[1]: "Category"})
        df['Source'] = destination
        df_out = pd.concat([df, df_out])
    
    for key, value in cat_dict.items():
    	df_out['Category'].loc[df_out['Category']==key] = value
    
    df_out = df_out[['Title', 'Datetime', 'Source', 'Category']]  
    
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
    
    delete_statement = f"DELETE FROM {dest_table} WHERE DATETIME < NOW() - INTERVAL '7 DAY'"
    
    query = insert + columns_string + ')\n     VALUES\n' + values_string[:-2] + ';' + '\n' + delete_statement + ';'
    
    return {'df_out': df_out.to_dict()}, {'timestamp': df['Datetime'].max()}, {'query': query}