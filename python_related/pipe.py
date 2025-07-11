
import pandas as pd
import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    dbname="getir",
    user="mert",
    password="password",
    port="5432"
)

# Your SQL query
query = """
SELECT 
  nearest_warehouse,
  MIN(delivery_duration) AS min_duration,
  MAX(delivery_duration) AS max_duration,
  AVG(delivery_duration) AS avg_duration,
  STDDEV_POP(delivery_duration) AS std_dev_pop,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY delivery_duration) AS median_duration
FROM siparis
GROUP BY nearest_warehouse;

"""

# Load query result into DataFrame
df = pd.read_sql(query, conn)

conn.close()

# Preview the data
print(df.head())
