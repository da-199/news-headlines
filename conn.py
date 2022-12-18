import psycopg2
import sys
import boto3
import os

ENDPOINT=""
PORT="5432"
USER=""
DBNAME=""
PASSWORD = "" 
# enter secrets above

def conn(query):
    try:
        conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USER, password=PASSWORD, sslrootcert="SSLCERTIFICATE")
        cur = conn.cursor()
        cur.execute(query)
        query_results = cur.fetchall()
        print(query_results)
    except Exception as e:
        print("Failed due to {}".format(e))    
    conn.commit()
    conn.close()
    cur.close()
