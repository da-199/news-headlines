import psycopg2
from get_secrets import get_secrets

def conn(event, context):

    secret_name = "postgres_connection"
    secret = get_secrets(secret_name)

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