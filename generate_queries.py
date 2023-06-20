import json
import psycopg2
import pandas as pd
import re
import sys
import boto3
import os

def combine_queries(event, context):
    
    separator = "\x1E"
    queries = [df_queries(event[x], x) for x in event.keys()]
    final_query = separator.join(queries) + separator + word_count_queries() + separator + junction_table_query()  + separator +  create_view()

    return {'query': final_query, 'separator': separator}

def df_queries(event, dest_table):
    
    df = event
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
        
    df_queries = insert + columns_string + ')\n     VALUES\n' + values_string[:-2] + ';' + '\n' + ';'

    return df_queries
    
def word_count_queries():
    
    query = """
    INSERT INTO word_count (word, count)
    SELECT word, count FROM (
      SELECT word, sum(count) as count 
      FROM staging_word_count 
      GROUP BY word
    ) as staging
    ON CONFLICT (word) DO UPDATE SET count = word_count.count + excluded.count;
    """
    
    return query
    
def junction_table_query():
    
    query = """
        drop table junction cascade; 

        create table junction as ( 
        	select * from (
        		select
        		w.id as word_count_id,
        		d.id as headline_id
        		from word_count as w
        		join (
        		SELECT regexp_replace(c.word, '''s$', '') AS word, c.id
        		from (
        				select REGEXP_REPLACE(b.word, '[0-9]', '', 'g') as word, b.id
        				from (
        					SELECT REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(a.word, '-', ''), '‘', ''), '’', ''), '—', ''), '(', ''), ')', ''), '+', ''), ';', ''), '&', ''), '!', ''), '$', ''), '?', ''), ':', ''), '.', ''), ',', '') AS word, id
        					from (
        						SELECT lower(regexp_split_to_table(title, ' ')) AS word, id
        						from v2_headline  
        					) as a
        				) as b
        			) as c
        		) as d
        		on w.word = d.word
        	) as g
        );
    """
    
    return query

def create_view():
    query = """
    create or replace view v2_headline_view as (
    SELECT j.word_count_id,
        j.headline_id,
        w.word,
        w.count,
        h.title,
        h.datetime,
        h.source,
        h.category
    FROM junction j
    JOIN word_count w ON j.word_count_id = w.id
    JOIN v2_headline h ON j.headline_id = h.id
    );

    """
    
    return query
    