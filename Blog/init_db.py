import os
import psycopg2
from dotenv import load_dotenv, find_dotenv
import sqlparse 

load_dotenv(find_dotenv())

conn = psycopg2.connect(
  port=5432,
  host=os.getenv('HOST'),
  dbname=os.getenv('DBNAME'),
  user=os.getenv('DB_USERNAME'),
  password=os.getenv('DB_PASSWORD')
)

cur = conn.cursor()

with open(r'c:\Users\admin\Downloads\flask-project\Blog\schema.sql', 'r', encoding='utf-8') as f:
	sql = f.read()
	commands = sqlparse.split(sql)

	for command in commands:
		command = command.strip()
		if command:
			cur.execute(command)


conn.commit()
cur.close()
conn.close()

print("Table is created!.")