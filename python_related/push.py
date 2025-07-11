import pandas as pd
from sqlalchemy import create_engine

# Parameters
db_user = 'mert'
dbuser_password = 'password'
db_host = 'localhost'
db_port = '5432'
db_name = 'getir'

# CSV file path siparisler ve warehouse csv dosyalari icin en az birer kez çalıştırılmalı
csv_file = 'C:\Python_Works\py\getir\getir_case_files\warehouse.csv'

# Read CSV into DataFrame
df = pd.read_csv(csv_file, sep = ',')
print(df.columns)
print(df.head())

# Create connection engine
engine = create_engine(f'postgresql://{db_user}:{dbuser_password}@{db_host}:{db_port}/{db_name}')

# Push DataFrame to PostgreSQL (replace 'employees' table)
df.to_sql('warehouse', engine, if_exists='replace', index= False)

print("CSV data pushed to PostgreSQL successfully!")
