from dotenv import load_dotenv
import pandas as pd
import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus

load_dotenv()

USER = os.getenv("user")
PASSWORD = quote_plus(os.getenv("password"))
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")


def query_database_to_dataframe():
    try:
        db_url = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
        engine = create_engine(db_url)
        with engine.connect() as connection:
            df = pd.read_sql_query("SELECT * FROM transactions;", connection)
        return df
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
