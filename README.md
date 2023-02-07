[Data Sources](https://github.com/dhruvi-9/news-headlines/tree/main/sources):
- New York Times Homepage API
- NBC News website

ETL Overview:

  ![Data Portfolio Diagram drawio](https://user-images.githubusercontent.com/100179105/217364381-b3e247b2-837e-4b54-ab0a-5e092b5d2835.png)

AWS Lambda Extraction & Processing Overview:
1. Files in sources folder are scheduled to scrape data from the different data source and outputs them into a dataframe.
2. insert_query.py turns dataframes into SQL insert queries, guided by definitions in the table_definitions folder.
3. database_connection.py connects to PostgreSQL and runs the SQL queries. 

  <img width="372" alt="Screen Shot 2023-01-27 at 12 13 29 AM" src="https://user-images.githubusercontent.com/100179105/215014391-1b6f34b7-e392-48c9-9900-a0b5c4b59a3b.png">


[Google Data Studio Visualization](https://lookerstudio.google.com/u/0/reporting/214b0ce7-0ee1-4702-9ded-160814a080a0/page/qA9CD):
  
  <img width="864" alt="Screen Shot 2023-01-30 at 1 08 20 AM" src="https://user-images.githubusercontent.com/100179105/215400508-55b05a90-2dbc-4401-8741-2106fb319001.png">
