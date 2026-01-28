import os
import datetime
import time
import psycopg2
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def get_db_connection():
    return psycopg2.connect(
		port=5432,
		host=os.getenv('HOST'),
		dbname=os.getenv('DBNAME'),
		user=os.getenv('DB_USERNAME'),
		password=os.getenv('DB_PASSWORD')
	)