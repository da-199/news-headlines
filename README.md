The data sources for are this are the following:
- New York Times Homepage API
- NBC News website

ETL Overview:

1. Files in sources folder are scheduled to scrape data from different sources and output them into a dataframe.
2. insert_query.py turns dataframes into SQL insert queries, guided by definitions in the table_definitions folder.
3. database_connection.py connects to PostgreSQL and runs the SQL queries. 

  <img width="372" alt="Screen Shot 2023-01-27 at 12 13 29 AM" src="https://user-images.githubusercontent.com/100179105/215014391-1b6f34b7-e392-48c9-9900-a0b5c4b59a3b.png">

[Google Data Studio Visualization](https://lookerstudio.google.com/u/0/reporting/214b0ce7-0ee1-4702-9ded-160814a080a0/page/qA9CD):
