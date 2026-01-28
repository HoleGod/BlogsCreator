import os
import psycopg2
from dotenv import load_dotenv, find_dotenv
import sqlparse 
from .db import get_db_connection

load_dotenv(find_dotenv())

conn = get_db_connection()

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