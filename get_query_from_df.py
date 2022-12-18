import re

def get_insert_query_from_df(df, dest_table):

    insert = """
    INSERT INTO public.{dest_table} (
        """.format(dest_table=dest_table)
    
    columns_string = str(list(df.columns))[1:-1]
    columns_string = re.sub(r' ', '\n        ', columns_string)
    columns_string = re.sub(r'\'', '', columns_string)

    values_string = ''
    df['Title'] = df['Title'].str.replace(r"'", '’', regex=True)

    for row in df.itertuples(index=False,name=None):
        row = re.sub(r'"', "'", str(row))
        values_string += re.sub(r'nan', 'null', str(row))
        values_string += ',\n'

    return insert + columns_string + ')\n     VALUES\n' + values_string[:-2] + ';'
