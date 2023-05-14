[Data Sources](https://github.com/dhruvi-9/news-headlines/tree/main/sources):
- New York Times Homepage API
- NBC News front page 
- ABC News front page

ETL Architecture Overview:

  <p align="center">
  <img width="952" height="183" src=https://github.com/dhruvi-9/news-headlines/assets/100179105/7e216cff-2fe4-4332-8b01-7dd73ae117e1
>
  </p>

  1. Files in the [sources](https://github.com/dhruvi-9/news-headlines/tree/main/sources) folder are scheduled to extract data on an hourly basis at the start of the hour.
  2. generate_queries.py turns the data into SQL insert queries and s3_output.py outputs a csv of the dataframe in an S3 bucket.
  3. database_connection.py loads the data to PostgreSQL by running the queries. 

[Google Data Studio Visualization](https://lookerstudio.google.com/u/0/reporting/78afc346-af31-485e-b6c9-e88ddebdfe8b/page/qA9CD)
