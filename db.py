from dotenv import load_dotenv
import pandas as pd
import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus

load_dotenv()

USER = os.getenv("user")
PASSWORD = quote_plus(str(os.getenv("password") or ""))
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")


def query_database_to_dataframe():
    try:
        if not all([USER, PASSWORD, HOST, PORT, DBNAME]):
            missing = [var for var, val in zip(
                ["user", "password", "host", "port", "dbname"],
                [USER, PASSWORD, HOST, PORT, DBNAME]
            ) if not val]
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

        port_str = str(PORT)

        db_url = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{port_str}/{DBNAME}?sslmode=require"
        engine = create_engine(db_url)
        with engine.connect() as connection:
            transactions_df = pd.read_sql_query("SELECT * FROM transactions;", connection)
            joined_data_df = pd.read_sql_query("""
                SELECT
                    t.id AS "ID da Transação",
                    COALESCE(u.full_name, u.username) AS "Nome Completo",
                    u.email AS "Email",
                    u.phone AS "Telefone",
                    u.referred_by AS "Recomendado por",
                    t.quantity_coin AS "Quantidade de Frevos",
                    t.transaction_status AS "Status da Transação",
                    t.created_at AS "Data da Criação"
                FROM transactions AS t
                JOIN transactions_user_lnk AS link ON t.id = link.transaction_id
                JOIN up_users AS u ON link.user_id = u.id;
                """, connection)
        return transactions_df, joined_data_df
    except ValueError as ve:
        print(f"Enviroment error: {ve}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None
