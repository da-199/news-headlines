[Data Sources](https://github.com/dhruvi-9/news-headlines/tree/main/sources):
- New York Times Homepage API
- NBC News front page 

ETL Architecture Overview:

            ![Data Portfolio Diagram](https://user-images.githubusercontent.com/100179105/222882276-ad4767d6-648c-4274-a3d0-        
            ce4c5f731b75.jpg)

  1. Files in the [sources](https://github.com/dhruvi-9/news-headlines/tree/main/sources) folder are scheduled to extract data on an hourly basis at the start of the hour.
  2. insert_query.py turns the data into SQL insert queries.
  3. database_connection.py loads the data to PostgreSQL by running the queries. 

[Google Data Studio Visualization](https://lookerstudio.google.com/u/0/reporting/214b0ce7-0ee1-4702-9ded-160814a080a0/page/qA9CD)
